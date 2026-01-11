# tests/test_upload.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.utils import generate_dummy_pdf, generate_empty_pdf
from io import BytesIO

@pytest.fixture
def client():
    return TestClient(app)

@pytest.mark.parametrize("file_name, file_content, content_type", [
    ("sample.pdf", generate_dummy_pdf(), "application/pdf"),
])
def test_upload_pdf(client, file_name, file_content, content_type):
    """
    Test uploading a valid PDF file.
    """
    response = client.post(
        "/api/v1/upload",
        files={"file": (file_name, file_content, content_type)}
    )
    assert response.status_code == 200
    data = response.json()
    # Updated assertion to match your endpoint response
    assert "chunks" in data
    assert "message" in data
    assert "uploaded" in data["message"]  # Ensure the message confirms upload

def test_upload_invalid_file(client):
    fake_file = BytesIO(b"Not a real PDF")
    response = client.post(
        "/api/v1/upload",
        files={"file": ("fake.txt", fake_file, "text/plain")}
    )
    assert response.status_code in [400, 422]
    assert "Document extraction failed" in response.text or "PDF" in response.text

def test_upload_empty_pdf(client):
    empty_pdf = generate_empty_pdf()
    response = client.post(
        "/api/v1/upload",
        files={"file": ("empty.pdf", empty_pdf, "application/pdf")}
    )
    assert response.status_code in [200, 400]
