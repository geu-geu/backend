from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.auth.domain.user import User
from app.auth.repositories.user_repository_impl import (
    IUserRepository,
    UserRepositoryImpl,
)
from app.auth.services.auth_service import AuthService
from app.config import settings
from app.database import SessionDep


def user_repository():
    return UserRepositoryImpl()


UserRepositoryDep = Annotated[IUserRepository, Depends(user_repository)]


def auth_service(user_repository: UserRepositoryDep):
    return AuthService(user_repository=user_repository)


AuthServiceDep = Annotated[AuthService, Depends(auth_service)]


async def get_current_user(
    token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/api/auth/login"))],
    user_repository: UserRepositoryDep,
    session: SessionDep,
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = user_repository.find_by_email(session, email=email)
    if not user:
        raise credentials_exception
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


async def get_current_active_user(current_user: CurrentUserDep) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user


CurrentActiveUserDep = Annotated[User, Depends(get_current_active_user)]
