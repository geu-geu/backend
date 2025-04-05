from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from fastapi import HTTPException, status
from sqlmodel import Session

from app.auth.domain.token import Token
from app.auth.domain.user import User
from app.auth.repositories.user_repository import IUserRepository
from app.config import settings
from app.security import verify_password

BEARER = "Bearer"


class AuthService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def login(self, session: Session, email: str, password: str) -> Token:
        user = self.__authenticate_user(session, email=email, password=password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": BEARER},
            )
        access_token = self.__create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        return Token(access_token=access_token, token_type=BEARER)

    def __authenticate_user(
        self, session: Session, email: str, password: str
    ) -> User | None:
        user = self.user_repository.find_by_email(session, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def __create_access_token(
        self,
        data: dict[str, Any],
        expires_delta: timedelta | None = None,
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            payload=to_encode,
            key=settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
        return encoded_jwt
