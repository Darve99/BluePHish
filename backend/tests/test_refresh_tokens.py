from app.auth import AuthService, UserCreate


def test_register_returns_refresh_token():
    auth_service = AuthService()
    result = auth_service.register(UserCreate(name="Alice", email="alice@test.com", password="password123"))

    assert "access_token" in result
    assert "refresh_token" in result
    assert result["user"]["email"] == "alice@test.com"


def test_login_returns_refresh_token():
    auth_service = AuthService()
    auth_service.register(UserCreate(name="Bob", email="bob@test.com", password="password123"))

    from app.auth import UserLogin

    result = auth_service.login(UserLogin(email="bob@test.com", password="password123"))

    assert "access_token" in result
    assert "refresh_token" in result


def test_refresh_token_creates_new_access_token():
    auth_service = AuthService()
    register_result = auth_service.register(UserCreate(name="Charlie", email="charlie@test.com", password="password123"))
    old_access_token = register_result["access_token"]
    refresh_token = register_result["refresh_token"]

    new_tokens = auth_service.refresh_access_token(refresh_token)

    assert new_tokens["access_token"] != old_access_token
    assert new_tokens["refresh_token"] != refresh_token


def test_user_has_role():
    auth_service = AuthService()
    result = auth_service.register(UserCreate(name="Dave", email="dave@test.com", password="password123"))

    assert result["user"].role == "user"
