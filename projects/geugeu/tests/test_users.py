from datetime import UTC, datetime

from sqlmodel import Session

from app.api.dependencies import get_current_user
from app.main import app
from app.models import User


def test_create_user(client):
    # given
    email = "user@example.com"
    password = "P@ssw0rd1234"

    # when
    response = client.post("/api/users", json={"email": email, "password": password})

    # then
    assert response.status_code == 201
    assert response.json()["email"] == email


def test_get_me(client, session):
    # given
    user = create_user(session, "user@example.com", "P@ssw0rd1234")
    app.dependency_overrides[get_current_user] = lambda: user

    # when
    response = client.get("/api/users/me")

    # then
    assert response.status_code == 200
    assert response.json()["email"] == user.email
    assert response.json()["code"] == user.code
    assert response.json()["profile_image_url"] == user.profile_image_url
    assert response.json()["created_at"] == user.created_at.isoformat().replace(
        "+00:00", "Z"
    )
    assert response.json()["updated_at"] == user.updated_at.isoformat().replace(
        "+00:00", "Z"
    )


def test_update_me(client, session):
    # given
    old_nickname = "old"
    new_nickname = "new"

    user = create_user(session, "user@example.com", "P@ssw0rd1234", old_nickname)
    app.dependency_overrides[get_current_user] = lambda: user

    # when
    response = client.put("/api/users/me", json={"nickname": new_nickname})

    # then
    assert response.status_code == 200
    assert response.json()["nickname"] == new_nickname


def test_delete_me(client, session):
    # given
    user = create_user(session, "user@example.com", "P@ssw0rd1234")
    assert user.is_active is True
    app.dependency_overrides[get_current_user] = lambda: user

    # when
    response = client.delete("/api/users/me")

    # then
    assert response.status_code == 204
    session.refresh(user)
    assert user.is_active is False


def create_user(
    session: Session, email: str, password: str, nickname: str | None = None
) -> User:
    user = User(
        code="abcd123",
        email=email,
        password=password,
        nickname=nickname,
        is_active=True,
        is_admin=False,
        profile_image_url=None,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    session.add(user)
    return user
