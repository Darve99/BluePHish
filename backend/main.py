from typing import Annotated, Optional

from fastapi import Depends, FastAPI, File, Form, HTTPException, Response, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

try:
    from app.admin import admin_service
    from app.ai_service import ai_service
    from app.analysis import analyzer
    from app.auth import AuthError, RegisterResponse, TokenResponse, User, UserCreate, UserLogin, auth_service, get_current_user
    from app.history import history_service
    from app.reporting import report_service
except Exception:
    admin_service = None
    ai_service = None
    analyzer = None
    auth_service = None
    history_service = None
    report_service = None
    AuthError = Exception
    TokenResponse = None
    User = None
    UserCreate = None
    UserLogin = None
    get_current_user = None

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


@app.post("/auth/register", response_model=RegisterResponse)
def register(user_data: UserCreate):
    if auth_service is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Auth service unavailable")
    try:
        return auth_service.register(user_data)
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@app.post("/auth/login", response_model=TokenResponse)
def login(credentials: UserLogin):
    if auth_service is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Auth service unavailable")
    try:
        return auth_service.login(credentials)
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@app.get("/auth/me", response_model=User)
def me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


class RefreshTokenRequest(BaseModel):
    refresh_token: str


@app.post("/auth/refresh", response_model=TokenResponse)
def refresh_token(payload: RefreshTokenRequest):
    return auth_service.refresh_access_token(payload.refresh_token)


class EmailAnalysisRequest(BaseModel):
    raw_email: str
    subject: Optional[str] = None
    has_attachment: Optional[bool] = False


@app.post("/analysis")
def analyze_email(payload: EmailAnalysisRequest, current_user: Annotated[User, Depends(get_current_user)]):
    if analyzer is None or ai_service is None or history_service is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Analysis service unavailable")
    result = analyzer.analyze(payload.raw_email)
    # prefer provided subject when given
    if payload.subject:
        result["subject"] = payload.subject
    # bump score if user indicated an attachment
    if payload.has_attachment:
        result["score"] = min(100, (result.get("score") or 0) + 10)
        score = result.get("score", 0)
        result["risk_level"] = "high" if score >= 70 else ("medium" if score >= 30 else "low")
    ai_result = ai_service.generate_analysis_summary(result)
    result["ai"] = ai_result
    history_service.add_entry(current_user.email, result)
    return result


@app.post("/analysis/guest")
def analyze_guest(payload: EmailAnalysisRequest):
    if analyzer is None or ai_service is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Analysis service unavailable")
    result = analyzer.analyze(payload.raw_email)
    if payload.subject:
        result["subject"] = payload.subject
    if payload.has_attachment:
        result["score"] = min(100, (result.get("score") or 0) + 10)
        score = result.get("score", 0)
        result["risk_level"] = "high" if score >= 70 else ("medium" if score >= 30 else "low")
    ai_result = ai_service.generate_analysis_summary(result)
    result["ai"] = ai_result
    return result


@app.post("/analysis/upload")
def upload_email(
    file: Annotated[UploadFile, File(...)],
    current_user: Annotated[User, Depends(get_current_user)],
    subject: Optional[str] = Form(None),
    has_attachment: bool = Form(False),
):
    if analyzer is None or ai_service is None or history_service is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Analysis service unavailable")
    if not file.filename or not file.filename.lower().endswith(".eml"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only .eml files are supported")

    content = file.file.read()
    result = analyzer.analyze(content)
    if subject:
        result["subject"] = subject
    if has_attachment:
        result["score"] = min(100, (result.get("score") or 0) + 10)
        score = result.get("score", 0)
        result["risk_level"] = "high" if score >= 70 else ("medium" if score >= 30 else "low")
    ai_result = ai_service.generate_analysis_summary(result)
    result["ai"] = ai_result
    history_service.add_entry(current_user.email, result)
    return result


@app.post("/analysis/guest/upload")
def upload_guest(
    file: Annotated[UploadFile, File(...)],
    subject: Optional[str] = Form(None),
    has_attachment: bool = Form(False),
):
    if analyzer is None or ai_service is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Analysis service unavailable")
    if not file.filename or not file.filename.lower().endswith(".eml"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only .eml files are supported")

    content = file.file.read()
    result = analyzer.analyze(content)
    if subject:
        result["subject"] = subject
    if has_attachment:
        result["score"] = min(100, (result.get("score") or 0) + 10)
        score = result.get("score", 0)
        result["risk_level"] = "high" if score >= 70 else ("medium" if score >= 30 else "low")
    ai_result = ai_service.generate_analysis_summary(result)
    result["ai"] = ai_result
    return result


@app.get("/history")
def list_history(current_user: Annotated[User, Depends(get_current_user)]):
    if history_service is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="History service unavailable")
    return history_service.list_for_user(current_user.email)


@app.post("/report")
def download_report(payload: EmailAnalysisRequest, current_user: Annotated[User, Depends(get_current_user)]):
    if analyzer is None or ai_service is None or report_service is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Report service unavailable")
    result = analyzer.analyze(payload.raw_email)
    ai_result = ai_service.generate_analysis_summary(result)
    result["ai"] = ai_result
    pdf_bytes = report_service.build_pdf(result)
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=bluephish-report-{current_user.id}.pdf"})


@app.get("/admin/stats")
def admin_stats(current_user: Annotated[User, Depends(get_current_user)]):
    if admin_service is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Admin service unavailable")
    return admin_service.stats()


@app.get("/admin/rules")
def admin_rules(current_user: Annotated[User, Depends(get_current_user)]):
    if admin_service is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Admin service unavailable")
    return admin_service.list_rules()


@app.put("/admin/rules/{rule_id}")
def update_rule(rule_id: str, weight: int, current_user: Annotated[User, Depends(get_current_user)]):
    if admin_service is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Admin service unavailable")
    return admin_service.update_rule(rule_id, weight)


@app.get("/admin/users")
def admin_users(current_user: Annotated[User, Depends(get_current_user)]):
    if admin_service is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Admin service unavailable")
    return admin_service.list_users()
