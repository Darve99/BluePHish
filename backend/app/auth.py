from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

SECRET_KEY = "dev-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer(auto_error=False)


class User(BaseModel):
    id: int
    name: str
    email: EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AuthError(Exception):
    pass


class AuthService:
    def __init__(self) -> None:
        self._users: dict[str, dict] = {}
        self._next_id = 1

    def register(self, user_data: UserCreate) -> dict:
        if user_data.email in self._users:
            raise AuthError("User already exists")

        hashed_password = pwd_context.hash(user_data.password)
        user = {
            "id": self._next_id,
            "name": user_data.name,
            "email": str(user_data.email),
            "password_hash": hashed_password,
        }
        self._users[str(user_data.email)] = user
        self._next_id += 1
        return {
            "user": User(**{k: v for k, v in user.items() if k != "password_hash"}),
            "access_token": self._create_access_token(user["email"]),
        }

    def login(self, credentials: UserLogin) -> dict:
        user = self._users.get(str(credentials.email))
        if not user or not pwd_context.verify(credentials.password, user["password_hash"]):
            raise AuthError("Invalid credentials")
        return {
            "access_token": self._create_access_token(user["email"]),
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

        user = self._users.get(email)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return User(id=user["id"], name=user["name"], email=user["email"])

    def _create_access_token(self, email: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": email, "exp": expire}
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


auth_service = AuthService()


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> User:
    return auth_service.get_current_user(credentials)
