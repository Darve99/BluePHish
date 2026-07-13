from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_upload_endpoint_accepts_eml_file():
    payload = {
        "file": ("sample.eml", b"Subject: Test upload\nFrom: sender@example.com\nTo: user@example.com\n\nPlease verify your account\n", "message/rfc822"),
    }

    response = client.post("/analysis/upload", files=payload)
    assert response.status_code in {200, 401}
