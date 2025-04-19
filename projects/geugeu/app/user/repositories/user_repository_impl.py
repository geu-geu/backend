from typing import final, override

from sqlmodel import Session, select

from app.models import User as _User
from app.user.domain.user import User
from app.user.repositories.user_repository import IUserRepository


@final
class UserRepositoryImpl(IUserRepository):
    @override
    def save(self, session: Session, user: User) -> None:
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
        session.add(_user)
        session.commit()

    @override
    def find_by_id(self, session: Session, id: str) -> User | None:
        _user = session.exec(select(_User).where(_User.id == id)).first()
        if not _user:
            return None
        return User(**_user.model_dump())

    @override
    def update(self, session: Session, user: User) -> User:
        _user = session.exec(select(_User).where(_User.id == user.id)).first()
        if not _user:
            raise ValueError(f"User with id {user.id} not found")
        _user.email = user.email
        _user.name = user.name
        _user.password = user.password
        _user.is_admin = user.is_admin
        _user.is_active = user.is_active
        _user.is_verified = user.is_verified
        _user.profile_image_url = user.profile_image_url
        _user.updated_at = user.updated_at
        session.add(_user)
        session.commit()
        session.refresh(_user)
        return User(**_user.model_dump())
