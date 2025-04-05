from typing import override

from sqlmodel import Session, select

from app.auth.domain.user import User
from app.auth.repositories.user_repository import IUserRepository
from app.models import User as _User


class UserRepositoryImpl(IUserRepository):
    @override
    def find_by_email(self, session: Session, email: str) -> User | None:
        _user = session.exec(select(_User).where(_User.email == email)).first()
        if not _user:
            return None
        return User(
            id=_user.id,
            email=_user.email,
            password=_user.password,
            is_active=_user.is_active,
            is_admin=_user.is_admin,
        )
