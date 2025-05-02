from datetime import UTC, datetime

import pytest

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


def test_create_user_with_existing_email(client, session):
    # given
    email = "user@example.com"
    password = "P@ssw0rd1234"

    user = User(
        email=email,
        password="$2b$12$g6AeAJXUJmaOcyYwUFVqgeeDL4UOnPVPuAXjSgqmgw/ZuTztFwAe.",
    )
    session.add(user)
    session.flush()

    # when
    response = client.post("/api/users", json={"email": email, "password": password})

    # then
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"


def test_create_user_with_deleted_email(client, session):
    # given
    email = "user@example.com"
    password = "P@ssw0rd1234"

    user = User(
        email=email,
        password="$2b$12$g6AeAJXUJmaOcyYwUFVqgeeDL4UOnPVPuAXjSgqmgw/ZuTztFwAe.",
        deleted_at=datetime.now(UTC),
    )
    session.add(user)
    session.flush()

    # when
    response = client.post("/api/users", json={"email": email, "password": password})

    # then
    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot sign up with this email"


def test_create_user_with_invalid_email(client):
    # given
    email = "user"
    password = "P@ssw0rd1234"

    # when
    response = client.post("/api/users", json={"email": email, "password": password})

    # then
    assert response.status_code == 422


@pytest.mark.parametrize(
    "password",
    [
        "P@ssw0r",  # 8자 이상 미충족
        "p@ssw0rd1234",  # 대문자 포함 미충족
        "P@SSW0RD1234",  # 소문자 포함 미충족
        "P@sswXrdXXXX",  # 숫자 포함 미충족
        "PAssw0rd1234",  # 특수문자 포함 미충족
    ],
)
def test_create_user_with_invalid_password(client, password):
    # given
    email = "user@example.com"

    # when
    response = client.post("/api/users", json={"email": email, "password": password})

    # then
    assert response.status_code == 422


def test_get_me(client, authorized_user):
    # when
    response = client.get("/api/users/me")

    # then
    assert response.status_code == 200
    assert response.json()["email"] == authorized_user.email
    assert response.json()["code"] == authorized_user.code
    assert response.json()["profile_image_url"] == authorized_user.profile_image_url
    assert response.json()[
        "created_at"
    ] == authorized_user.created_at.isoformat().replace("+00:00", "Z")
    assert response.json()[
        "updated_at"
    ] == authorized_user.updated_at.isoformat().replace("+00:00", "Z")


def test_get_me_401(client, user):
    # when
    response = client.get("/api/users/me")

    # then
    assert response.status_code == 401


def test_update_me(client, authorized_user):
    # given
    new_nickname = "geugeugood"

    # when
    response = client.put("/api/users/me", json={"nickname": new_nickname})

    # then
    assert response.status_code == 200
    assert response.json()["nickname"] == new_nickname


def test_update_me_401(client, user):
    # given
    new_nickname = "geugeugood"

    # when
    response = client.put("/api/users/me", json={"nickname": new_nickname})

    # then
    assert response.status_code == 401


def test_delete_me(client, session, authorized_user):
    assert authorized_user.deleted_at is None

    # when
    response = client.delete("/api/users/me")

    # then
    assert response.status_code == 204
    session.refresh(authorized_user)
    assert authorized_user.deleted_at is not None


def test_delete_me_401(client, user):
    # when
    response = client.delete("/api/users/me")

    # then
    assert response.status_code == 401
