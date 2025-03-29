from collections.abc import Generator
from datetime import UTC, datetime

import pytest
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel
from ulid import ULID

from app.security import hash_password
from app.user.application.user_service import UserService
from app.user.domain.user import User
from app.user.domain.user_repository import IUserRepository
from app.user.infrastructure.user_repository import UserRepository


@pytest.fixture()
def user_repository() -> IUserRepository:
    return UserRepository()


@pytest.fixture()
def user_service(user_repository: IUserRepository) -> UserService:
    return UserService(user_repository=user_repository)


@pytest.fixture()
def session() -> Generator[Session, None, None]:
    _engine = create_engine("sqlite:///sqlite3.db")
    SQLModel.metadata.create_all(_engine)
    with Session(_engine) as session:
        yield session
    SQLModel.metadata.drop_all(_engine)


def test_signup(user_service: UserService, session: Session) -> None:
    # given
    email = "user@example.com"
    password = "P@ssw0rd"

    # when
    new_user = user_service.signup(session=session, email=email, password=password)

    # then
    assert len(new_user.id) == 26
    assert new_user.email == email
    assert new_user.password != password
    assert len(new_user.password) == 60
    assert new_user.name is None
    assert new_user.is_admin is False
    assert new_user.is_active is True
    assert new_user.created_at is not None
    assert new_user.updated_at is not None


def test_get_user(
    user_service: UserService, user_repository: IUserRepository, session: Session
) -> None:
    # given
    user_id = str(ULID())
    user = User(
        id=user_id,
        email="user@example.com",
        name=None,
        password=hash_password("password"),
        is_admin=False,
        is_active=True,
        is_verified=False,
        profile_image_url=None,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    user_repository.save(session, user)

    # when
    result = user_service.get_user(session, user_id)

    # then
    assert result == user
