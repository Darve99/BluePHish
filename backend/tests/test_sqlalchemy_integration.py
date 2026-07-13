import pytest

from app.auth import UserCreate
from app.auth import auth_service as auth_service_instance
from app.db_persistence import db_persistence
from app.database import Base, SessionLocal, engine
from app.history import history_service


@pytest.fixture(autouse=True)
def setup_db():
    """Create tables before each test and drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_register_user_creates_db_entry():
    result = auth_service_instance.register(
        UserCreate(name="Alice", email="alice@test.com", password="password123")
    )

    assert result["user"].email == "alice@test.com"
    assert result["access_token"]
    assert result["refresh_token"]

    # Verify user in database
    user = db_persistence.get_user_by_email("alice@test.com")
    assert user is not None
    assert user.name == "Alice"
    assert user.role == "user"


def test_login_with_db():
    from app.auth import UserLogin

    auth_service_instance.register(
        UserCreate(name="Bob", email="bob@test.com", password="password123")
    )

    result = auth_service_instance.login(
        UserLogin(email="bob@test.com", password="password123")
    )

    assert result["access_token"]
    assert result["refresh_token"]


def test_analysis_history_persists():
    auth_service_instance.register(
        UserCreate(name="Charlie", email="charlie@test.com", password="password123")
    )

    analysis = {
        "subject": "Test Email",
        "score": 75.0,
        "risk_level": "high",
        "summary": "This is a test",
        "indicators": ["urgent_language", "shortened_url"],
    }

    history_service.add_entry("charlie@test.com", analysis)

    user_history = history_service.list_for_user("charlie@test.com")
    assert len(user_history) == 1
    assert user_history[0]["subject"] == "Test Email"
    assert user_history[0]["score"] == 75.0


def test_multiple_users_isolated():
    auth_service_instance.register(
        UserCreate(name="Dave", email="dave@test.com", password="password123")
    )
    auth_service_instance.register(
        UserCreate(name="Eve", email="eve@test.com", password="password123")
    )

    analysis1 = {
        "subject": "Email 1",
        "score": 50.0,
        "risk_level": "medium",
        "summary": "Test 1",
        "indicators": [],
    }
    analysis2 = {
        "subject": "Email 2",
        "score": 90.0,
        "risk_level": "high",
        "summary": "Test 2",
        "indicators": ["phishing"],
    }

    history_service.add_entry("dave@test.com", analysis1)
    history_service.add_entry("eve@test.com", analysis2)

    dave_history = history_service.list_for_user("dave@test.com")
    eve_history = history_service.list_for_user("eve@test.com")

    assert len(dave_history) == 1
    assert len(eve_history) == 1
    assert dave_history[0]["score"] == 50.0
    assert eve_history[0]["score"] == 90.0
