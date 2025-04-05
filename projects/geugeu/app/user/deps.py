from typing import Annotated

from fastapi import Depends

from app.user.repositories.user_repository import IUserRepository
from app.user.repositories.user_repository_impl import UserRepositoryImpl
from app.user.services.user_service import UserService


def user_repository():
    return UserRepositoryImpl()


UserRepositoryDep = Annotated[IUserRepository, Depends(user_repository)]


def user_service(user_repository: UserRepositoryDep):
    return UserService(user_repository=user_repository)


UserServiceDep = Annotated[UserService, Depends(user_service)]
