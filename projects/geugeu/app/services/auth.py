import time
from datetime import timedelta

import httpx
import jwt
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token
from app.models import User
from app.schemas.auth import AppleToken, GoogleToken, GoogleUser, Token


def get_user_by_code(db: Session, code: str) -> User | None:
    return db.execute(
        select(User).where(
            User.code == code,
            User.deleted_at.is_(None),
        )
    ).scalar_one_or_none()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.execute(
        select(User).where(
            User.email == email,
            User.deleted_at.is_(None),
        )
    ).scalar_one_or_none()


def google_login(db: Session, code: str, redirect_uri: str) -> Token:
    # 구글 액세스 토큰 요청
    response = httpx.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        },
    )
    google_token = GoogleToken.model_validate(response.json())

    # 구글 계정 조회 및 이메일 추출
    response = httpx.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={
            "Authorization": f"{google_token.token_type} {google_token.access_token}"
        },
    )
    google_user = GoogleUser.model_validate(response.json())

    # 구글 계정이 인증되지 않은 경우 예외 처리
    if not google_user.verified_email:
        raise HTTPException(status_code=401, detail="Google account is not verified")

    # 이메일로 유저 조회
    user = db.execute(
        select(User).where(User.email == google_user.email)
    ).scalar_one_or_none()

    # 유저가 삭제된 경우 예외 처리
    if user and user.deleted_at:
        raise HTTPException(status_code=401, detail="Cannot sign in with this email")

    # 유저가 없으면 생성
    if not user:
        user = User(
            email=google_user.email,
            nickname=google_user.name,
            password=None,
            is_admin=False,
            profile_image_url=google_user.picture,
            auth_provider=User.AuthProvider.GOOGLE,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # 해당 유저의 토큰 발행
    return Token(
        access_token=create_access_token(user.code, expires_delta=timedelta(days=1)),
        token_type="Bearer",
    )


def apple_login(db: Session, code: str, redirect_uri: str) -> Token:
    client_secret = _generate_apple_client_secret()
    response = httpx.post(
        "https://appleid.apple.com/auth/oauth2/v2/token",
        data={
            "client_id": settings.APPLE_CLIENT_ID,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        },
    )
    apple_token = AppleToken.model_validate(response.json())
    data = jwt.decode(apple_token.id_token, options={"verify_signature": False})
    email = data["email"]

    if not data["email_verified"]:
        raise HTTPException(status_code=401, detail="Apple account is not verified")

    # 이메일로 유저 조회
    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()

    # 유저가 삭제된 경우 예외 처리
    if user and user.deleted_at:
        raise HTTPException(status_code=401, detail="Cannot sign in with this email")

    # 유저가 없으면 생성
    if not user:
        user = User(
            email=email,
            password=None,
            is_admin=False,
            auth_provider=User.AuthProvider.APPLE,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return Token(
        access_token=create_access_token(user.code, expires_delta=timedelta(days=1)),
        token_type="Bearer",
    )


def _generate_apple_client_secret():
    headers = {
        "alg": "ES256",
        "kid": settings.APPLE_KEY_ID,
    }
    payload = {
        "iss": settings.APPLE_TEAM_ID,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
        "aud": "https://appleid.apple.com",
        "sub": settings.APPLE_CLIENT_ID,
    }
    token = jwt.encode(
        payload=payload,
        key=settings.APPLE_PRIVATE_KEY,
        algorithm="ES256",
        headers=headers,
    )
    return token
