from fastapi import UploadFile, HTTPException
from app.repositories.file_repository import FileRepository


class FileService:
    def __init__(self, repository: FileRepository):
        self.repository = repository

    def upload_pdf(self, file: UploadFile) -> dict:
        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported"
            )

        saved_path = self.repository.save_pdf(file)

        return {
            "filename": file.filename,
            "status": "uploaded",
            "path": str(saved_path)
        }
