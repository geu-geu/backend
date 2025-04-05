from datetime import UTC, datetime

import pytest
from sqlmodel import Session
from ulid import ULID

from app.security import hash_password
from app.user.api.schemas.users import SignupBody
from app.user.domain.user import User
from app.user.repositories.user_repository import IUserRepository
from app.user.repositories.user_repository_impl import UserRepositoryImpl
from app.user.services.user_service import UserService


@pytest.fixture()
def user_repository() -> IUserRepository:
    return UserRepositoryImpl()


@pytest.fixture()
def user_service(user_repository: IUserRepository) -> UserService:
    return UserService(user_repository=user_repository)


def test_signup(user_service: UserService, session: Session) -> None:
    # given
    signup_body = SignupBody(email="user@example.com", password="P@ssw0rd")

    # when
    new_user = user_service.signup(session, signup_body)

    # then
    assert len(new_user.id) == 26
    assert new_user.email == signup_body.email
    assert new_user.password != signup_body.password
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
