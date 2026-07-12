from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.auth import AuthError, TokenResponse, User, UserCreate, UserLogin, auth_service, get_current_user

app = FastAPI(title="BluePHish API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/auth/register", response_model=dict)
def register(user_data: UserCreate):
    try:
        return auth_service.register(user_data)
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@app.post("/auth/login", response_model=TokenResponse)
def login(credentials: UserLogin):
    try:
        return auth_service.login(credentials)
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@app.get("/auth/me", response_model=User)
def me(current_user: User = Depends(get_current_user)):
    return current_user
