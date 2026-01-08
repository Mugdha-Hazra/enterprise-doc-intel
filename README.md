# Enterprise Document Intelligence API

## 1. Project Setup (Foundation)

### Actions Taken:

1. **Created project folder**

   ```
   C:\Users\KIIT\enterprise-doc-intel
   ```

   with subfolders:

   * `backend/` → Python FastAPI backend
   * `android/` → future mobile client
   * `README.md` → project documentation

2. **Initialized Git repository**

   ```bat
   git init
   git branch -M main
   ```

   * Enables **version control** and incremental commits.

3. **Created Python virtual environment**

   ```bat
   python -m venv venv
   venv\Scripts\activate
   ```

   * Isolated project dependencies
   * Prevents conflicts with system Python

4. **Installed dependencies** (via `requirements.txt`):

   * `fastapi` → backend framework
   * `uvicorn` → ASGI server for FastAPI
   * `pydantic` → data validation
   * `python-multipart` → file upload handling
   * Additional packages: `shutil`, `pathlib` (built-in), etc.

5. **Backend folder structure**

   ```
   backend/
       app/
           main.py
       data/                  # PDF storage
       venv/
       requirements.txt
   ```

6. **Verified FastAPI Health Check**

   * Endpoint: `/api/v1/health`
   * Response: `{"status":"ok"}`
   * Confirms backend is **running correctly**.

---

## 2. GitHub Integration

* Repository created and linked to local repo
* First commit pushed
* Credential caching enabled
* Outcome: **Remote backup + version tracking**

---

## 3. Project Architecture

<img width="857" height="573" alt="image" src="https://github.com/user-attachments/assets/ead5a71f-a73f-44da-b4dc-51275b140229" />

<img width="876" height="592" alt="image" src="https://github.com/user-attachments/assets/9c944eac-6ca0-432e-bd96-3999439457b1" />


**Description:**

* Clients (Web/Mobile) interact with **FastAPI backend**
* Routes available under `/api/v1/`:

  * `/health` → checks server status
  * `/upload` → accepts PDF files only
* Uploaded PDFs stored in **`backend/data/`**
* Swagger UI provides **interactive API testing**
* Backend designed for **enterprise-level data separation and offline-first operation**

---

## 4. Phase 2: Document Upload Feature

### Step 1: Storage Preparation

* Created `backend/data/` folder
* Added to `.gitignore` → prevents committing user data
* Mimics **enterprise-grade separation of data**.

---

### Step 2: Add `/upload` Endpoint

**Python Implementation:**

```python
@app.post("/api/v1/upload")
def upload_document(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    destination = DATA_DIR / file.filename
    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "status": "uploaded"}
```

**Step-by-Step Explanation:**

1. **`@app.post("/api/v1/upload")`**

   * Receives **POST requests** with file upload.
2. **File Handling**

   * `UploadFile` provides filename, file stream, and MIME type.
3. **Validation**

   * Ensures only **PDF files** are accepted.
4. **File Storage**

   * Streams file to `backend/data/` safely.
5. **Response**

   * Returns JSON confirming successful upload.

---

### Step 3: Swagger UI

* Navigate: `http://127.0.0.1:8000/docs`
* Interactive API testing:

  * `/api/v1/health` → GET
  * `/api/v1/upload` → POST (PDF only)
* Allows **quick validation of endpoints**.

---

## 5. Current Status

| Feature                            | Status                      |
| ---------------------------------- | --------------------------- |
| Project Folder & Backend Setup     | ✅ Completed                 |
| Git + GitHub Integration           | ✅ Completed                 |
| Virtual Environment & Dependencies | ✅ Completed                 |
| `/api/v1/health` endpoint          | ✅ Working                   |
| `/api/v1/upload` endpoint          | ✅ Working (PDF only)        |
| Swagger UI                         | ✅ Interactive testing ready |
| File storage (`backend/data/`)     | ✅ Working                   |
| API versioning `/api/v1/`          | ✅ Implemented               |

**Notes:**

* Attempted `/api/v1/upload` via GET → **405 Method Not Allowed** (expected behavior)
* Accessing `/upload` outside `/api/v1/` → **404 Not Found** (ensures versioned API)

---

## 6. Future Enhancements

1. **Document Processing Pipeline**

   * Extract text and metadata from uploaded PDFs
   * Store parsed data in a structured database

2. **Authentication & Authorization**

   * JWT / OAuth2 integration
   * Role-based access for users

3. **Mobile Client Integration**

   * Android client to upload and retrieve documents
   * Interactive UI for document management

4. **Advanced Features**

   * PDF annotation, search, and categorization
   * Dashboard with analytics on uploaded documents

---

## 7. Quick Start

1. Clone repository:

```bash
git clone <repo-url>
cd enterprise-doc-intel/backend
```

2. Activate virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run FastAPI server:

```bash
uvicorn app.main:app --reload
```

5. Access Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

✅ **Project ready for enterprise-grade PDF upload and API testing**

---

