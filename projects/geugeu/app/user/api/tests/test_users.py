from datetime import UTC, datetime
from unittest.mock import patch

from fastapi.testclient import TestClient
from ulid import ULID

from app.main import app
from app.user.application.user_service import UserService
from app.user.domain.entity.user import User

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
