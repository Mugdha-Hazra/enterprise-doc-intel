import pytest
from fastapi.testclient import TestClient
from io import BytesIO
from reportlab.pdfgen import canvas
from app.main import app
from tests.utils import generate_dummy_pdf, generate_empty_pdf


# -------------------------------
# Fixtures
# -------------------------------
@pytest.fixture(scope="module")
def client():
    """Provides a test client for the FastAPI app."""
    with TestClient(app) as c:
        yield c

# -------------------------------
# Helper functions
# -------------------------------
def generate_dummy_pdf(text="Hello, World!"):
    """Generate an in-memory PDF for testing."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, text)
    c.save()
    buffer.seek(0)
    return buffer

def generate_empty_pdf():
    """Generate an in-memory empty PDF."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.save()
    buffer.seek(0)
    return buffer

# -------------------------------
# Health Endpoint
# -------------------------------
def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"

# -------------------------------
# Search Endpoint
# -------------------------------
def test_search_endpoint_no_results(client):
    """Test search endpoint when no documents match."""
    response = client.post("/api/v1/search?query=test&top_k=3")
    assert response.status_code == 200
    results = response.json()
    # The API returns a dict with 'answer' and 'sources'
    assert isinstance(results, dict)
    assert "answer" in results
    assert "sources" in results
    assert results["sources"] == []

# -------------------------------
# Upload Endpoint
# -------------------------------
@pytest.mark.parametrize(
    "file_name, file_content, content_type",
    [
        ("sample.pdf", generate_dummy_pdf(), "application/pdf"),  # valid PDF
        ("empty.pdf", generate_empty_pdf(), "application/pdf"),   # empty PDF
    ]
)
def test_upload_pdf(client, file_name, file_content, content_type):
    """Test uploading a valid or empty PDF file."""
    response = client.post(
        "/api/v1/upload",
        files={"file": (file_name, file_content, content_type)}
    )
    # The valid PDF should succeed; empty PDF may fail based on your API
    if file_name == "sample.pdf":
        assert response.status_code == 200
    elif file_name == "empty.pdf":
        assert response.status_code in [400, 422]

def test_upload_invalid_file(client):
    """Test uploading a non-PDF file."""
    fake_file = BytesIO(b"Not a real PDF")
    response = client.post(
        "/api/v1/upload",
        files={"file": ("fake.txt", fake_file, "text/plain")}
    )
    # API should reject non-PDF files
    assert response.status_code in [400, 422]
    # Check that the error message mentions 'PDF' or 'Document extraction'
    assert any(keyword in response.text for keyword in ["PDF", "Document extraction"])
