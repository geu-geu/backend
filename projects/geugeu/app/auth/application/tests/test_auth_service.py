from typing import Any

import pytest
from pytest_mock import MockerFixture
from ulid import ULID

from app.auth.application.auth_service import AuthService
from app.auth.domain.user import User
from app.auth.domain.user_repository import IUserRepository
from app.security import hash_password


@pytest.fixture()
def user_repository(mocker: MockerFixture) -> Any:
    return mocker.Mock(spec=IUserRepository)


@pytest.fixture()
def auth_service(user_repository: IUserRepository) -> AuthService:
    return AuthService(user_repository=user_repository)


def test_login(auth_service: AuthService) -> None:
    # given
    email = "user@example.com"
    password = "P@ssw0rd"
    auth_service.user_repository.find_by_email.return_value = User(
        id=str(ULID()),
        email=email,
        password=hash_password(password),
        is_admin=False,
        is_active=True,
    )

    # when
    token = auth_service.login(email=email, password=password)

    # then
    assert token.access_token is not None
    assert token.token_type == "Bearer"
