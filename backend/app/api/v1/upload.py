from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Validate content type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    # Phase 1: no persistence, no processing
    return {
        "status": "uploaded",
        "filename": file.filename
    }
