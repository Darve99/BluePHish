from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_analysis_endpoint_returns_risk_and_indicators():
    response = client.post(
        "/analysis",
        json={
            "raw_email": "Subject: Urgent password reset\nFrom: no-reply@security-support.com\nTo: user@example.com\n\nPlease verify your password immediately."
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["score"] >= 0
    assert payload["risk_level"] in {"low", "medium", "high"}
    assert payload["urls"] == []
    assert payload["subject"] == "Urgent password reset"
    assert isinstance(payload.get("rule_hits"), list)
    assert len(payload["rule_hits"]) >= 2
