from datetime import timedelta
from typing import Annotated
from urllib.parse import urljoin

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import create_access_token, verify_password
from app.schemas.auth import Token
from app.services import auth as service

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_db)],
):
    user = service.get_user_by_email(session, form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not verify_password(form_data.password, user.password or ""):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return Token(
        access_token=create_access_token(user.code, expires_delta=timedelta(days=1)),
        token_type="Bearer",
    )


@router.get(
    "/google",
    response_model=Token,
    description="""
Google에서 호출하는 콜백 API입니다. 구글 로그인을 시작하려면 아래 API를 호출하세요.

GET https://accounts.google.com/o/oauth2/v2/auth

Query Parameters:
- client_id: <client_id>
- redirect_uri: https://geugeu.com/api/auth/google
- response_type: code
- scope: https://www.googleapis.com/auth/userinfo.email
- state: <random_string>
""",
)
async def google_oauth_callback(
    session: Annotated[Session, Depends(get_db)],
    request: Request,
    code: str = Query(...),
):
    # TODO: state 검증 (CSRF 공격 방지)
    redirect_uri = urljoin(str(request.base_url), "/api/auth/google")
    return service.google_login(session, code, redirect_uri)
