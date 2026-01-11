import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_endpoint(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"service": "enterprise-doc-intel", "status": "healthy"}
