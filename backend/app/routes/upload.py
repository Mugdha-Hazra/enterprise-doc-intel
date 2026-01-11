# app/routes/upload.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_pipeline import DocumentPipeline
import shutil
import os
import uuid

router = APIRouter(prefix="/api/v1", tags=["Upload"])

UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

pipeline = DocumentPipeline()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_id = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, file_id)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process document
    extracted_data = pipeline.process(file_path)

    extracted_text = extracted_data.get("text")

    if not extracted_text:
        raise HTTPException(
            status_code=400,
            detail="Document extraction failed. No text found."
        )

    return {
        "message": "Document uploaded and indexed successfully",
        "chunks": extracted_data.get("chunks")
    }
