from typing import override

from sqlmodel import Session, select

from app.auth.domain.user import User
from app.auth.domain.user_repository import IUserRepository
from app.database import engine
from app.models import User as _User


class UserRepository(IUserRepository):
    @override
    def find_by_email(self, email: str) -> User | None:
        with Session(engine) as session:
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
