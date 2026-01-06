# ==========================================
# Enterprise Document Intelligence System
# Backend Main Application
# ==========================================
# This FastAPI backend allows:
# 1. Health check endpoint (/health)
# 2. PDF upload endpoint (/upload)
#    - Saves PDF to local disk
#    - Extracts text from PDF using PyMuPDF (fitz)
#    - Saves extracted text as .txt in the same folder
#
# Directory Structure:
# backend/
# ├─ app/
# │  └─ main.py      <- This file
# ├─ data/           <- Stores uploaded PDFs and extracted text
# └─ venv/           <- Python virtual environment
# ==========================================

# -------------------------------
# Imports (All at the Top)
# -------------------------------
from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import fitz  # PyMuPDF for PDF text extraction

# -------------------------------
# FastAPI Application Setup
# -------------------------------
app = FastAPI(title="Enterprise Document Intelligence System")

# -------------------------------
# Define Base Directories
# -------------------------------
# BASE_DIR: Points to backend folder (one level above 'app')
BASE_DIR = Path(__file__).resolve().parent.parent

# DATA_DIR: Folder to store uploaded PDFs and extracted text files
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)  # Create 'data' folder if it doesn't exist

# -------------------------------
# Root Endpoint
# -------------------------------
@app.get("/")
def root():
    """
    Root endpoint.
    Purpose:
    - Quick sanity check that the API is running
    - Helpful for browsers, load balancers, and monitoring tools
    """
    return {
        "service": "Enterprise Document Intelligence API",
        "status": "running",
        "version": "0.1.0"
    }


# -------------------------------
# Health Check Endpoint
# -------------------------------
@app.get("/health")
def health_check():
    """
    Simple GET endpoint to verify backend is running.
    Returns JSON {"status": "ok"}.
    Useful for:
      - Monitoring server status
      - Quick sanity check after deployment
    """
    return {"status": "ok"}

# -------------------------------
# PDF Upload and Text Extraction Endpoint
# -------------------------------
@app.post("/upload")
def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF file, save it locally, extract text, and save text as .txt.
    
    Workflow:
    1. Validate uploaded file is a PDF
    2. Save PDF to 'data/' folder
    3. Open PDF using PyMuPDF
    4. Extract text from all pages
    5. Save extracted text as .txt in 'data/' folder
    6. Return JSON response with status and text filename
    """

    # -------------------------------
    # Step 1: Validate File Type
    # -------------------------------
    if file.content_type != "application/pdf":
        # Raise error if file is not a PDF
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    # -------------------------------
    # Step 2: Save PDF to Disk
    # -------------------------------
    pdf_path = DATA_DIR / file.filename  # Full path to save PDF
    with pdf_path.open("wb") as buffer:
        # Copy uploaded file's stream to disk safely
        shutil.copyfileobj(file.file, buffer)

    # -------------------------------
    # Step 3: Extract Text from PDF
    # -------------------------------
    pdf_document = fitz.open(pdf_path)  # Open the PDF file
    text_content = ""
    for page in pdf_document:           # Iterate through all pages
        text_content += page.get_text() # Extract text per page
    pdf_document.close()                 # Close PDF to free memory

    # -------------------------------
    # Step 4: Save Extracted Text
    # -------------------------------
    txt_filename = file.filename.replace(".pdf", ".txt")  # Keep same name
    txt_path = DATA_DIR / txt_filename
    with txt_path.open("w", encoding="utf-8") as f:
        f.write(text_content)  # Save extracted text to disk

    # -------------------------------
    # Step 5: Return Response
    # -------------------------------
    return {
        "filename": file.filename,   # Original PDF filename
        "status": "uploaded",        # Upload status
        "text_file": txt_filename    # Generated text file
    }

# ==========================================
# End of main.py
# ==========================================
