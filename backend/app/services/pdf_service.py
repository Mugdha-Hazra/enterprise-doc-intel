# app/services/pdf_service.py

from PyPDF2 import PdfReader

class PDFService:
    """
    Extracts text from PDF files using PyPDF2
    """
    def extract_text(self, file_path: str) -> str:
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text.strip()
        except Exception as e:
            print(f"PDF extraction failed: {e}")
            return ""
