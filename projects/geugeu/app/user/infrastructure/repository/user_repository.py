from typing import final, override

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.database import engine
from app.user.domain.entity.user import User
from app.user.domain.repository.user_repository import IUserRepository
from app.user.infrastructure.model.user import User as _User


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
    def find_by_email(self, email: str) -> User:
        with Session(engine) as session:
            _user = session.exec(select(_User).where(_User.email == email)).first()
        if not _user:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return User(**_user.model_dump())
