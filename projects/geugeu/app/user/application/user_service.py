from datetime import UTC, datetime

from ulid import ULID

from app.security import hash_password
from app.user.domain.entity.user import User
from app.user.domain.repository.user_repository import IUserRepository


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
        self.user_repository.save(user)
        return user
