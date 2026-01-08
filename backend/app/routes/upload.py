import os # Import os module for file path operations
from fastapi import APIRouter, UploadFile, File # Import necessary FastAPI components, including APIRouter for route grouping and file upload handling
from datetime import datetime # Import datetime for timestamping uploads
from app.services.pdf_service import extract_text_from_pdf # Import the PDF text extraction service

router = APIRouter(prefix="/api/v1") # Initialize APIRouter instance

UPLOAD_DIR = "data" # Directory to save uploaded files
os.makedirs(UPLOAD_DIR, exist_ok=True) # Ensure the upload directory exists

@router.post("/upload") # Define the upload endpoint
async def upload_document(file: UploadFile = File(...)): # Function to handle document uploads
    file_path = os.path.join(UPLOAD_DIR, file.filename) # Define the file path to save the uploaded file

    with open(file_path, "wb") as f: # Open the file in write-binary mode
        f.write(await file.read()) # Write the uploaded file's content to disk

    extracted_data = extract_text_from_pdf(file_path) # Extract text from the uploaded PDF using the service

    return { # Return response with upload details and extracted data
        "file_name": file.filename,
        "uploaded_at": datetime.utcnow().isoformat(),
        "pages": extracted_data["total_pages"],
        "status": "processed"
    }
