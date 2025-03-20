from datetime import UTC, datetime
from unittest.mock import patch

from fastapi.testclient import TestClient
from ulid import ULID

from app.auth.dependencies import get_current_active_user
from app.main import app
from app.user.application.user_service import UserService
from app.user.domain.user import User

client = TestClient(app)


@patch.object(UserService, "signup")
def test_signup(signup):
    # given
    payload = {"email": "user@example.com", "password": "P@ssw0rd1234"}

    user = User(
        id=str(ULID()),
        email=payload["email"],
        name=None,
        password=payload["password"],
        is_admin=False,
        is_active=True,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    signup.return_value = user

    # when
    response = client.post("/api/users/signup", json=payload)

    # then
    assert response.status_code == 201
    assert response.json()["id"] == user.id
    assert response.json()["email"] == user.email


@patch.object(UserService, "get_user")
def test_get_user(get_user):
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
    get_user.return_value = user

    def override_get_current_active_user():
        return user

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user

    # when
    response = client.get(f"/api/users/{user_id}")

    # then
    assert response.status_code == 200
    assert response.json()["id"] == user_id
