from datetime import UTC, datetime
from typing import Any

import pytest
from pytest_mock import MockerFixture
from ulid import ULID

from app.user.application.user_service import UserService
from app.user.domain.user import User
from app.user.domain.user_repository import IUserRepository


@pytest.fixture()
def user_repository(mocker: MockerFixture) -> Any:
    return mocker.Mock(spec=IUserRepository)


@pytest.fixture()
def user_service(user_repository: IUserRepository) -> UserService:
    return UserService(user_repository=user_repository)


def test_signup(user_service: UserService) -> None:
    # given
    email = "user@example.com"
    password = "P@ssw0rd"

    # when
    new_user = user_service.signup(email=email, password=password)

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


def test_get_user(user_service) -> None:
    # given
    user_id = str(ULID())
    user = User(
        id=user_id,
        email="user@example.com",
        name=None,
        password="password",
        is_admin=False,
        is_active=True,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    user_service.user_repository.find_by_id.return_value = user

    # when
    result = user_service.get_user(user_id)

    # then
    assert result == user
