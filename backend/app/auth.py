from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.db_persistence import db_persistence
from app.models import UserDB

SECRET_KEY = "dev-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
bearer_scheme = HTTPBearer(auto_error=False)


class User(BaseModel):
    id: int
    name: str
    email: str
    role: str = "user"


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RegisterResponse(BaseModel):
    user: User
    access_token: str
    refresh_token: str


class AuthError(Exception):
    pass


class AuthService:
    def __init__(self) -> None:
        # No need to load users from file - they're in the database
        pass

    def register(self, user_data: UserCreate) -> dict:
        if db_persistence.get_user_by_email(str(user_data.email)):
            raise AuthError("User already exists")

        hashed_password = pwd_context.hash(user_data.password)
        user = db_persistence.create_user(
            name=user_data.name,
            email=str(user_data.email),
            password_hash=hashed_password,
            role="user",
        )
        return {
            "user": User(id=user.id, name=user.name, email=user.email, role=user.role),
            "access_token": self._create_access_token(user.email),
            "refresh_token": self._create_refresh_token(user.email),
        }

    def login(self, credentials: UserLogin) -> dict:
        user = db_persistence.get_user_by_email(str(credentials.email))
        if not user or not pwd_context.verify(credentials.password, user.password_hash):
            raise AuthError("Invalid credentials")
        return {
            "access_token": self._create_access_token(user.email),
            "refresh_token": self._create_refresh_token(user.email),
            "token_type": "bearer",
        }

    def refresh_access_token(self, refresh_token: str) -> dict:
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
            if not email or payload.get("type") != "refresh":
                raise HTTPException(status_code=401, detail="Invalid refresh token")
        except JWTError as exc:
            raise HTTPException(status_code=401, detail="Invalid refresh token") from exc

        user = db_persistence.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return {
            "access_token": self._create_access_token(email),
            "refresh_token": self._create_refresh_token(email),
            "token_type": "bearer",
        }

    def get_current_user(self, credentials: Optional[HTTPAuthorizationCredentials]) -> User:
        if not credentials:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        try:
            payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
            if not email:
                raise HTTPException(status_code=401, detail="Invalid token")
        except JWTError as exc:
            raise HTTPException(status_code=401, detail="Invalid token") from exc

        user = db_persistence.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return User(id=user.id, name=user.name, email=user.email, role=user.role)

    def _create_access_token(self, email: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": email, "exp": expire, "type": "access"}
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def _create_refresh_token(self, email: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        payload = {"sub": email, "exp": expire, "type": "refresh"}
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


auth_service = AuthService()


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> User:
    return auth_service.get_current_user(credentials)
