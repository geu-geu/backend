from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from ulid import ULID

from app.auth.deps import get_current_user
from app.main import app
from app.user.domain.user import User
from app.user.repositories.user_repository import IUserRepository
from app.user.repositories.user_repository_impl import UserRepositoryImpl

client = TestClient(app)


@pytest.fixture()
def user_repository():
    return UserRepositoryImpl()


@pytest.fixture()
def current_user():
    user = User(
        id=str(ULID()),
        email="user@example.com",
        name=None,
        password="password",
        is_admin=False,
        is_active=True,
        is_verified=False,
        profile_image_url=None,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    def override_get_current_user():
        return user

    app.dependency_overrides[get_current_user] = override_get_current_user
    yield user
    app.dependency_overrides.clear()


def test_signup():
    # given
    payload = {"email": "user@example.com", "password": "P@ssw0rd1234"}

    # when
    response = client.post("/api/users/signup", json=payload)

    # then
    assert response.status_code == 201
    assert response.json()["email"] == payload["email"]


def test_me(session: Session, user_repository: IUserRepository, current_user: User):
    # given
    user_repository.save(session, current_user)

    # when
    response = client.get("/api/users/me")

    # then
    assert response.status_code == 200
