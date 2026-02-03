import pdfplumber
from PIL import Image
import pytesseract
import os

tesseract_cmd = os.getenv("TESSERACT_CMD", "tesseract")  # fallback to default path if not set
pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

# ---------------- Functions ----------------

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

# ---------------- Test ----------------

if __name__ == "__main__":
    # Test PDF extraction
    pdf_file = "sample_referral.pdf"  # put a PDF path here
    try:
        pdf_text = extract_text_from_pdf(pdf_file)
        print("PDF Text Extraction Success:\n", pdf_text[:300], "...")  # print first 300 chars
    except Exception as e:
        print("PDF extraction failed:", e)

    # Test image extraction
    image_file = "sample_scan.png"  # put an image path here
    try:
        image_text = extract_text_from_image(image_file)
        print("Image OCR Extraction Success:\n", image_text[:300], "...")
    except Exception as e:
        print("Image OCR failed:", e)
