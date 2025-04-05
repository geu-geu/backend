from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.auth.domain.user import User
from app.auth.repositories.user_repository_impl import (
    IUserRepository,
    UserRepositoryImpl,
)
from app.auth.services.auth_service import AuthService
from app.database import SessionDep


def user_repository():
    return UserRepositoryImpl()


UserRepositoryDep = Annotated[IUserRepository, Depends(user_repository)]


def auth_service(user_repository: UserRepositoryDep):
    return AuthService(user_repository=user_repository)


AuthServiceDep = Annotated[AuthService, Depends(auth_service)]


async def get_current_user(
    token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/api/auth/login"))],
    auth_service: AuthServiceDep,
    session: SessionDep,
) -> User:
    return auth_service.get_current_user(token, session)


CurrentUserDep = Annotated[User, Depends(get_current_user)]
