from app.services.llm import llm
import json
import os
from typing import List, Optional
from pydantic import BaseModel, Field

# Try importing OCR tools, but don't fail if they are missing (handled at runtime)
try:
    import pdfplumber
    from PIL import Image
    import pytesseract
except ImportError:
    pdfplumber = None
    Image = None
    pytesseract = None

class PatientData(BaseModel):
    patient_name: Optional[str] = Field(None, description="Name of the patient")
    age: Optional[int] = Field(None, description="Age of the patient")
    symptoms: List[str] = Field(default_factory=list, description="List of symptoms reported")
    diagnosis: Optional[str] = Field(None, description="Diagnosis if mentioned, otherwise None")
    missing_info: List[str] = Field(default_factory=list, description="List of missing vital information")

def extract_text_from_pdf(file_path):
    if not pdfplumber:
        return "[Error: pdfplumber not installed]"
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        return f"[Error reading PDF: {str(e)}]"
    return text

def extract_text_from_image(file_path):
    if not pytesseract or not Image:
        return "[Error: pytesseract or Pillow not installed]"
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        # PytesseractError usually indicates binary missing
        return f"[Error executing OCR: {str(e)}. Ensure Tesseract is installed and in PATH.]"

def normalize_text(text):
    return " ".join(text.strip().split())

def intake_agent(state: dict):
    """
    Intake Agent: Handles text, PDF, or image input.
    Converts raw input into structured JSON using LLM with structured output.
    """
    raw_input = state.get("raw_input", "")
    file_input = state.get("file_input")

    # Extract text if file provided
    if file_input and os.path.exists(file_input):
        ext = os.path.splitext(file_input)[1].lower()
        extracted_text = ""
        if ext == ".pdf":
            extracted_text = extract_text_from_pdf(file_input)
        elif ext in [".png", ".jpg", ".jpeg"]:
            extracted_text = extract_text_from_image(file_input)
        
        if extracted_text:
            raw_input += f"\n[Extracted from File]: {extracted_text}"

    raw_input = normalize_text(raw_input)

    # Use structured output for reliability
    structured_llm = llm.with_structured_output(PatientData)
    
    prompt = f"Extract patient information from the following text:\n\n{raw_input}"
    
    try:
        result = structured_llm.invoke(prompt)
        structured_data = result.model_dump()
    except Exception as e:
        structured_data = {"error": "LLM parsing failed", "details": str(e)}

    return {"raw_input": raw_input, "structured_data": structured_data}
