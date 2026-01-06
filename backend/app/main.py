# ==========================================
# Enterprise Document Intelligence System
# Backend Main Application (FastAPI)
# ==========================================
# This backend provides:
# 1. Root endpoint ("/api/v1/") to check service status
# 2. Health check endpoint ("/api/v1/health")
# 3. PDF upload endpoint ("/api/v1/upload")
#    - Saves PDF to local disk
#    - Extracts text using PyMuPDF
#    - Saves extracted text as .txt in 'data' folder
#
# Directory Structure:
# backend/
# ├─ app/
# │  └─ main.py        <- This file
# ├─ data/             <- Stores PDFs and text files
# └─ venv/             <- Python virtual environment
# ==========================================

# -------------------------------
# Imports
# -------------------------------
from fastapi import FastAPI, UploadFile, File, HTTPException, APIRouter
from pathlib import Path
import shutil
import fitz  # PyMuPDF for PDF text extraction
import logging
from app.routes import health, upload
# -------------------------------
# Logging Configuration
# -------------------------------
# Logging prints messages with timestamp and level (INFO, WARNING, ERROR)
logging.basicConfig(
    level=logging.INFO,  # Show all INFO messages and above
    format="%(asctime)s [%(levelname)s] %(message)s",  # Message format
    handlers=[logging.StreamHandler()]  # Print logs to console
)
logger = logging.getLogger(__name__)

# -------------------------------
# FastAPI App Setup
# -------------------------------
app = FastAPI(title="Enterprise Document Intelligence System")


app.include_router(health.router)
app.include_router(upload.router)

# -------------------------------
# API Versioning
# -------------------------------
# All routes are prefixed with /api/v1
api_v1 = APIRouter(prefix="/api/v1")

# -------------------------------
# Directories Setup
# -------------------------------
# BASE_DIR points to backend folder (one level above 'app')
BASE_DIR = Path(__file__).resolve().parent.parent

# DATA_DIR is where PDFs and text files are stored
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)  # Create folder if it doesn't exist

# ==========================================
# Endpoints
# ==========================================

# -------------------------------
# Root Endpoint
# -------------------------------
@api_v1.get("/")
def root():
    """
    Root endpoint.
    Purpose:
      - Quick check that the API is running
      - Useful for browser access or monitoring tools
    Returns JSON with service status and version
    """
    logger.info("Root endpoint accessed")
    return {
        "service": "Enterprise Document Intelligence API",
        "status": "running",
        "version": "0.1.0"
    }

# -------------------------------
# Health Check Endpoint
# -------------------------------
@api_v1.get("/health")
def health_check():
    """
    Health check endpoint.
    Purpose:
      - Verify backend server is running
      - Useful for monitoring systems
    Returns JSON {"status": "ok"}
    """
    logger.info("Health check requested")
    return {"status": "ok"}

# -------------------------------
# PDF Upload Endpoint
# -------------------------------
@api_v1.post("/upload")
def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF, extract its text, and save as .txt file.

    Steps:
    1. Validate file is a PDF
    2. Save PDF to DATA_DIR
    3. Extract text from PDF using PyMuPDF
    4. Save text as a .txt file in DATA_DIR
    5. Return JSON response with status and filename
    """

    # -------------------------------
    # Step 1: Validate File Type
    # -------------------------------
    if file.content_type != "application/pdf":
        logger.warning(f"Rejected non-PDF file: {file.filename}")
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    # -------------------------------
    # Step 2: Save PDF to Disk
    # -------------------------------
    pdf_path = DATA_DIR / file.filename
    with pdf_path.open("wb") as buffer:
        # Copy uploaded file to disk
        shutil.copyfileobj(file.file, buffer)
    logger.info(f"PDF saved: {pdf_path}")

    # -------------------------------
    # Step 3: Extract Text from PDF
    # -------------------------------
    pdf_document = fitz.open(pdf_path)  # Open PDF
    text_content = ""
    for page in pdf_document:            # Go through each page
        text_content += page.get_text()  # Extract text
    pdf_document.close()                  # Close PDF to free memory
    logger.info(f"Text extracted from PDF: {pdf_path.name}")

    # -------------------------------
    # Step 4: Save Extracted Text
    # -------------------------------
    txt_filename = file.filename.replace(".pdf", ".txt")
    txt_path = DATA_DIR / txt_filename
    with txt_path.open("w", encoding="utf-8") as f:
        f.write(text_content)
    logger.info(f"Text file saved: {txt_path}")

    # -------------------------------
    # Step 5: Return JSON Response
    # -------------------------------
    return {
        "filename": file.filename,   # Original PDF filename
        "status": "uploaded",        # Upload status
        "text_file": txt_filename    # Generated text file
    }

# -------------------------------
# Include API Router in FastAPI App
# -------------------------------
app.include_router(api_v1)

# ==========================================
# End of main.py
# ==========================================
