from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_admin_endpoints_are_accessible():
    response = client.get("/admin/stats")
    assert response.status_code == 200

    rules_response = client.get("/admin/rules")
    assert rules_response.status_code == 200

    users_response = client.get("/admin/users")
    assert users_response.status_code == 200
