from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_report_endpoint_returns_pdf():
    response = client.post(
        "/report",
        json={"raw_email": "Subject: Urgent password reset\nFrom: support@example.com\nTo: user@example.com\n\nPlease verify your password immediately."},
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/pdf")
