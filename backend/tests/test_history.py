from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_history_endpoint_returns_saved_entries():
    register_response = client.post(
        "/auth/register",
        json={"name": "History User", "email": "history@example.com", "password": "secret"},
    )
    token = register_response.json()["access_token"]

    client.post(
        "/analysis",
        json={"raw_email": "Subject: Urgent password reset\nFrom: support@example.com\nTo: user@example.com\n\nPlease verify your password immediately."},
        headers={"Authorization": f"Bearer {token}"},
    )

    history_response = client.get(
        "/history",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert history_response.status_code == 200
    assert len(history_response.json()) >= 1
