from typing import Annotated

from fastapi import Depends

from app.auth.application.auth_service import AuthService
from app.auth.domain.user_repository import IUserRepository
from app.auth.infrastructure.user_repository import UserRepository


def user_repository():
    return UserRepository()


UserRepositoryDep = Annotated[IUserRepository, Depends(user_repository)]


def auth_service(user_repository: UserRepositoryDep):
    return AuthService(user_repository=user_repository)


AuthServiceDep = Annotated[AuthService, Depends(auth_service)]
