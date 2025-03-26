from typing import Generator

import pytest
from fastapi.testclient import TestClient
from ulid import ULID

from app.auth.dependencies import get_current_active_user
from app.auth.domain.user import User
from app.main import app


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def user() -> User:
    return User(
        id=str(ULID()),
        email="test@example.com",
        password="password",
        is_active=True,
        is_admin=False,
    )


@pytest.fixture(autouse=True)
def override_auth_dependency():
    def override_current_active_user_dep():
        return User(
            id=str(ULID()),
            email="user@example.com",
            password="password",
            is_admin=False,
            is_active=True,
        )

    app.dependency_overrides[get_current_active_user] = override_current_active_user_dep
    yield
    app.dependency_overrides.clear()
