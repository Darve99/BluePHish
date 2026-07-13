from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_analysis_includes_ai_block_when_no_api_key():
    response = client.post(
        "/analysis",
        json={
            "raw_email": "Subject: Urgent password reset\nFrom: no-reply@security-support.com\nTo: user@example.com\n\nPlease verify your password immediately."
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert "ai" in payload
    assert payload["ai"]["classification"] == "manual_review"
