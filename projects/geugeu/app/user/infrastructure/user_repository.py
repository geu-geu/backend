from typing import final, override

from sqlmodel import Session, select

from app.database import engine
from app.models import User as _User
from app.user.domain.user import User
from app.user.domain.user_repository import IUserRepository


@final
class UserRepository(IUserRepository):
    @override
    def save(self, user: User) -> None:
        _user = _User(
            id=user.id,
            email=user.email,
            name=user.name,
            password=user.password,
            is_admin=user.is_admin,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        with Session(engine) as session:
            session.add(_user)
            session.commit()

    @override
    def find_by_id(self, id: str) -> User | None:
        with Session(engine) as session:
            _user = session.exec(select(_User).where(_User.id == id)).first()
        if not _user:
            return None
        return User(**_user.model_dump())
