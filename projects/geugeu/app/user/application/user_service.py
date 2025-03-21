from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from ulid import ULID

from app.security import hash_password
from app.user.domain.user import User
from app.user.domain.user_repository import IUserRepository


class UserService:
    def __init__(self, user_repository: IUserRepository) -> None:
        self.user_repository = user_repository

    def signup(self, email: str, password: str, name: str | None = None) -> User:
        user = User(
            id=str(ULID()),
            email=email,
            password=hash_password(password),
            name=name,
            is_admin=False,
            is_active=True,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        try:
            self.user_repository.save(user)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists",
            )
        return user

    def get_user(self, id: str) -> User:
        user = self.user_repository.find_by_id(id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user
