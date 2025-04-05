from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from ulid import ULID

from app.security import hash_password
from app.user.domain.user import User
from app.user.repositories.user_repository import IUserRepository


class UserService:
    def __init__(self, user_repository: IUserRepository) -> None:
        self.user_repository = user_repository

    def signup(
        self, session: Session, email: str, password: str, name: str | None = None
    ) -> User:
        user = User(
            id=str(ULID()),
            email=email,
            password=hash_password(password),
            name=name,
            is_admin=False,
            is_active=True,
            is_verified=False,
            profile_image_url=None,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        try:
            self.user_repository.save(session, user)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists",
            )
        return user

    def get_user(self, session: Session, id: str) -> User:
        user = self.user_repository.find_by_id(session, id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user
