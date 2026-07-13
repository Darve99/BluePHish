from app.auth import AuthService, UserCreate
from app.history import HistoryService


def test_auth_and_history_persist_to_disk(tmp_path):
    from app import persistence as persistence_module

    persistence_module.persistence = persistence_module.FilePersistence(str(tmp_path))

    auth_service = AuthService()
    user = auth_service.register(UserCreate(name="Persist", email="persist@example.com", password="password123"))
    assert user["user"].email == "persist@example.com"

    history_service = HistoryService()
    history_service.add_entry("persist@example.com", {"subject": "Persisted", "score": 55, "risk_level": "medium", "summary": "Stored", "indicators": []})

    saved_history = persistence_module.persistence.load_json("history.json", [])
    assert len(saved_history) == 1
    assert saved_history[0]["subject"] == "Persisted"
