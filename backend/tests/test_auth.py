from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_register_login_and_me_flow():
    payload = {
        "name": "Alice Example",
        "email": "alice@example.com",
        "password": "super-secret",
    }

    register_response = client.post("/auth/register", json=payload)
    assert register_response.status_code == 200
    body = register_response.json()
    assert body["user"]["email"] == payload["email"]
    assert "access_token" in body

    login_response = client.post(
        "/auth/login",
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert login_response.status_code == 200
    tokens = login_response.json()
    assert tokens["access_token"]

    me_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == payload["email"]
