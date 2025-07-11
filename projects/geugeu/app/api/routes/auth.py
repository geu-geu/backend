from datetime import timedelta
from typing import Annotated
from urllib.parse import urljoin

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.core.dependencies import AuthServiceDep
from app.core.security import create_access_token, verify_password
from app.schemas.auth import Token

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthServiceDep,
):
    user = service.get_user_by_email(form_data.username)
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
    request: Request,
    service: AuthServiceDep,
    code: str = Query(...),
):
    # TODO: state 검증 (CSRF 공격 방지)
    redirect_uri = urljoin(str(request.base_url), "/api/auth/google")
    return service.google_login(code, redirect_uri)


@router.post(
    "/apple",
    response_model=Token,
    description="""
Apple에서 호출하는 콜백 API입니다. 애플 로그인을 시작하려면 아래 API를 호출하세요.

GET https://appleid.apple.com/auth/authorize

Query Parameters:
- client_id: <client_id>
- redirect_uri: https://geugeu.com/api/auth/apple
- response_type: code
- scope: name email
- state: <random_string>
- response_mode: form_post
""",
)
async def apple_oauth_callback(
    request: Request,
    service: AuthServiceDep,
    code: str = Form(...),
):
    redirect_uri = urljoin(str(request.base_url), "/api/auth/apple")
    return service.apple_login(code, redirect_uri)
