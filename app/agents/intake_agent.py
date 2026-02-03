from app.services.llm import llm
import json
import os
import pdfplumber
from PIL import Image
import pytesseract

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_image(file_path):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    return text

def normalize_text(text):
    return " ".join(text.strip().split())  # simple whitespace cleanup

def intake_agent(state: dict):
    """
    Intake Agent: Handles text, PDF, or image input.
    Converts raw input into structured JSON using LLM.
    """
    raw_input = state.get("raw_input", "")
    file_input = state.get("file_input")  # optional: path to PDF/image

    # Extract text if file provided
    if file_input:
        ext = os.path.splitext(file_input)[1].lower()
        if ext in [".pdf"]:
            extracted_text = extract_text_from_pdf(file_input)
        elif ext in [".png", ".jpg", ".jpeg"]:
            extracted_text = extract_text_from_image(file_input)
        else:
            extracted_text = ""
        raw_input += " " + extracted_text

    raw_input = normalize_text(raw_input)

    prompt = f"""
Extract the following from patient input and return ONLY JSON:
- patient_name (string)
- age (integer)
- symptoms (list of strings)
- diagnosis (string)
- missing_info (list of missing fields)

Text:
\"\"\"{raw_input}\"\"\"
"""

    response = llm.invoke(prompt)

    try:
        structured_data = json.loads(response)
    except json.JSONDecodeError:
        structured_data = {"error": "JSON parse failed", "raw_output": response}

    return {"raw_input": raw_input, "structured_data": structured_data}
