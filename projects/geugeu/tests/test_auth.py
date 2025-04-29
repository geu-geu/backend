from datetime import UTC, datetime

from sqlmodel import Session

from app.models import User


def test_login(client, session):
    # given
    create_user(
        session,
        email="user@example.com",
        password="$2b$12$g6AeAJXUJmaOcyYwUFVqgeeDL4UOnPVPuAXjSgqmgw/ZuTztFwAe.",
    )

    # when
    response = client.post(
        "/api/auth/login",
        data={"username": "user@example.com", "password": "P@ssw0rd1234"},
    )

    # then
    assert response.status_code == 200
    assert response.json()["access_token"].startswith("ey")
    assert response.json()["token_type"] == "Bearer"


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
