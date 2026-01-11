from io import BytesIO


def test_upload_pdf_success(client):
    fake_pdf = BytesIO(b"%PDF-1.4 fake pdf content")

    response = client.post(
        "/api/v1/upload",
        files={"file": ("test.pdf", fake_pdf, "application/pdf")},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "uploaded"
    assert response.json()["filename"] == "test.pdf"


def test_upload_rejects_non_pdf(client):
    fake_txt = BytesIO(b"not a pdf")

    response = client.post(
        "/api/v1/upload",
        files={"file": ("test.txt", fake_txt, "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF files are supported"
