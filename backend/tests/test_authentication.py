from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_register_and_me_flow():
    payload = {"name": "Alice", "email": "alice@example.com", "password": "secret123"}
    register_response = client.post("/auth/register", json=payload)
    assert register_response.status_code == 200

    login_response = client.post(
        "/auth/login",
        json={"email": "alice@example.com", "password": "secret123"},
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    me_response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "alice@example.com"
