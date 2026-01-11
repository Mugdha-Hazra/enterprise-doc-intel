# tests/test_search.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_search_endpoint(client):
    response = client.post("/api/v1/search?query=test&top_k=3")
    assert response.status_code == 200
    results = response.json()
    # Adjust based on your API response
    assert isinstance(results, dict)
    assert "answer" in results
    assert "sources" in results
