from typing import Annotated

from fastapi import Depends

from app.user.application.user_service import UserService
from app.user.domain.user_repository import IUserRepository
from app.user.infrastructure.user_repository import UserRepository


def user_repository():
    return UserRepository()


UserRepositoryDep = Annotated[IUserRepository, Depends(user_repository)]


def user_service(user_repository: UserRepositoryDep):
    return UserService(user_repository=user_repository)


UserServiceDep = Annotated[UserService, Depends(user_service)]
