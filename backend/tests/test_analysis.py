from fastapi.testclient import TestClient
import uuid

from main import app

client = TestClient(app)


def get_auth_token() -> str:
    suffix = uuid.uuid4().hex
    register_response = client.post(
        "/auth/register",
        json={"name": "Analysis Tester", "email": f"analysis+{suffix}@test.com", "password": "secret123"},
    )
    assert register_response.status_code == 200
    return register_response.json()["access_token"]


def test_analysis_endpoint_returns_risk_and_indicators():
    token = get_auth_token()
    response = client.post(
        "/analysis",
        json={
            "raw_email": "Subject: Urgent password reset\nFrom: no-reply@security-support.com\nTo: user@example.com\n\nPlease verify your password immediately."
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["score"] >= 0
    assert payload["risk_level"] in {"none", "low", "medium", "high"}
    assert payload["urls"] == []
    assert payload["subject"] == "Urgent password reset"
    assert isinstance(payload.get("rule_hits"), list)
    assert len(payload["rule_hits"]) >= 2


def test_analysis_endpoint_returns_none_risk_for_clean_email():
    token = get_auth_token()
    response = client.post(
        "/analysis",
        json={
            "raw_email": "Subject: Hello\nFrom: user@example.com\nTo: recipient@example.com\n\nEste es un mensaje de prueba sin indicios de phishing.",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["score"] == 0
    assert payload["risk_level"] == "none"
    assert payload["rule_hits"] == []
