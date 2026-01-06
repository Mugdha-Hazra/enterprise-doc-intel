import os
from fastapi import APIRouter, UploadFile, File
from datetime import datetime
from app.services.pdf_service import extract_text_from_pdf

router = APIRouter()

UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    extracted_data = extract_text_from_pdf(file_path)

    return {
        "file_name": file.filename,
        "uploaded_at": datetime.utcnow().isoformat(),
        "pages": extracted_data["total_pages"],
        "status": "processed"
    }
