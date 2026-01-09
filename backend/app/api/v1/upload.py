from fastapi import APIRouter, UploadFile, File
from app.core.config import DATA_DIR
from app.repositories.file_repository import FileRepository
from app.services.file_service import FileService

router = APIRouter(tags=["Upload"])

file_repository = FileRepository(DATA_DIR)
file_service = FileService(file_repository)


@router.post("/upload")
def upload_document(file: UploadFile = File(...)):
    return file_service.upload_pdf(file)
