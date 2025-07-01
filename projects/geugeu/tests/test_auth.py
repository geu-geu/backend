from datetime import UTC, datetime
from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.services.auth import apple_login, google_login


def test_login(client, user):
    # when
    response = client.post(
        "/api/auth/login",
        data={
            "username": user.email,
            "password": "P@ssw0rd1234",
        },
    )

    # then
    assert response.status_code == 200
    assert response.json()["access_token"].startswith("ey")
    assert response.json()["token_type"] == "Bearer"


def test_login_with_invalid_email(client, user, raw_password):
    # when
    response = client.post(
        "/api/auth/login",
        data={"username": "invalid_email", "password": raw_password},
    )

    # then
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_login_with_deleted_email(client, db, user, raw_password):
    # given
    user.deleted_at = datetime.now(UTC)
    db.flush()

    # when
    response = client.post(
        "/api/auth/login",
        data={"username": user.email, "password": raw_password},
    )

    # then
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_login_with_invalid_password(client, user):
    # when
    response = client.post(
        "/api/auth/login",
        data={"username": user.email, "password": "invalid_password"},
    )

    # then
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_google_login_success(client, db):
    """Google OAuth 로그인 성공 테스트"""
    # given
    mock_google_token_response = {
        "access_token": "mock_access_token",
        "expires_in": 3600,
        "scope": "openid email profile",
        "token_type": "Bearer",
        "id_token": "mock.id.token",
    }
    mock_google_user_response = {
        "id": "123456789",
        "email": "user@gmail.com",
        "name": "Test User",
        "picture": "https://example.com/profile.jpg",
        "verified_email": True,
    }

    with patch("httpx.post") as mock_post, patch("httpx.get") as mock_get:
        mock_post.return_value.json.return_value = mock_google_token_response
        mock_get.return_value.json.return_value = mock_google_user_response

        # when
        token = google_login(db, "mock_code", "http://localhost:3000/callback")

        # then
        assert token.access_token.startswith("ey")
        assert token.token_type == "Bearer"


def test_google_login_unverified_email(client, db):
    """Google OAuth 로그인 - 인증되지 않은 이메일 테스트"""
    # given
    mock_google_token_response = {
        "access_token": "mock_access_token",
        "expires_in": 3600,
        "scope": "openid email profile",
        "token_type": "Bearer",
        "id_token": "mock.id.token",
    }
    mock_google_user_response = {
        "id": "123456789",
        "email": "user@gmail.com",
        "name": "Test User",
        "verified_email": False,  # 인증되지 않은 이메일
    }

    with patch("httpx.post") as mock_post, patch("httpx.get") as mock_get:
        mock_post.return_value.json.return_value = mock_google_token_response
        mock_get.return_value.json.return_value = mock_google_user_response

        # when & then
        with pytest.raises(HTTPException) as exc_info:
            google_login(db, "mock_code", "http://localhost:3000/callback")

        assert exc_info.value.status_code == 401
        assert "not verified" in exc_info.value.detail


def test_google_login_with_deleted_user(client, db, user):
    """Google OAuth 로그인 - 삭제된 사용자 테스트"""
    # given
    user.deleted_at = "2023-01-01T00:00:00"
    db.commit()

    mock_google_token_response = {
        "access_token": "mock_access_token",
        "expires_in": 3600,
        "scope": "openid email profile",
        "token_type": "Bearer",
        "id_token": "mock.id.token",
    }
    mock_google_user_response = {
        "id": "123456789",
        "email": user.email,
        "name": "Test User",
        "verified_email": True,
    }

    with patch("httpx.post") as mock_post, patch("httpx.get") as mock_get:
        mock_post.return_value.json.return_value = mock_google_token_response
        mock_get.return_value.json.return_value = mock_google_user_response

        # when & then
        with pytest.raises(HTTPException) as exc_info:
            google_login(db, "mock_code", "http://localhost:3000/callback")

        assert exc_info.value.status_code == 401
        assert "Cannot sign in" in exc_info.value.detail


def test_apple_login_success(client, db):
    """Apple OAuth 로그인 성공 테스트"""
    # given
    mock_apple_token_response = {
        "access_token": "mock_access_token",
        "refresh_token": "mock_refresh_token",
        "id_token": "mock.id.token",
    }
    mock_id_token_payload = {
        "email": "user@icloud.com",
        "email_verified": True,
    }

    with patch("httpx.post") as mock_post, \
         patch("jwt.decode") as mock_jwt_decode, \
         patch("app.services.auth._generate_apple_client_secret") as mock_secret:

        mock_post.return_value.json.return_value = mock_apple_token_response
        mock_jwt_decode.return_value = mock_id_token_payload
        mock_secret.return_value = "mock_client_secret"

        # when
        token = apple_login(db, "mock_code", "http://localhost:3000/callback")

        # then
        assert token.access_token.startswith("ey")
        assert token.token_type == "Bearer"


def test_apple_login_unverified_email(client, db):
    """Apple OAuth 로그인 - 인증되지 않은 이메일 테스트"""
    # given
    mock_apple_token_response = {
        "access_token": "mock_access_token",
        "refresh_token": "mock_refresh_token",
        "id_token": "mock.id.token",
    }
    mock_id_token_payload = {
        "email": "user@icloud.com",
        "email_verified": False,  # 인증되지 않은 이메일
    }

    with patch("httpx.post") as mock_post, \
         patch("jwt.decode") as mock_jwt_decode, \
         patch("app.services.auth._generate_apple_client_secret") as mock_secret:

        mock_post.return_value.json.return_value = mock_apple_token_response
        mock_jwt_decode.return_value = mock_id_token_payload
        mock_secret.return_value = "mock_client_secret"

        # when & then
        with pytest.raises(HTTPException) as exc_info:
            apple_login(db, "mock_code", "http://localhost:3000/callback")

        assert exc_info.value.status_code == 401
        assert "not verified" in exc_info.value.detail


def test_google_oauth_endpoint(client, db):
    """Google OAuth 엔드포인트 테스트"""
    # given
    mock_google_token_response = {
        "access_token": "mock_access_token",
        "expires_in": 3600,
        "scope": "openid email profile",
        "token_type": "Bearer",
        "id_token": "mock.id.token",
    }
    mock_google_user_response = {
        "id": "123456789",
        "email": "newuser@gmail.com",
        "name": "New User",
        "verified_email": True,
    }

    with patch("httpx.post") as mock_post, patch("httpx.get") as mock_get:
        mock_post.return_value.json.return_value = mock_google_token_response
        mock_get.return_value.json.return_value = mock_google_user_response

        # when
        response = client.get("/api/auth/google?code=mock_auth_code")

        # then
        assert response.status_code == 200
        assert response.json()["access_token"].startswith("ey")
        assert response.json()["token_type"] == "Bearer"


def test_apple_oauth_endpoint(client, db):
    """Apple OAuth 엔드포인트 테스트"""
    # given
    mock_apple_token_response = {
        "access_token": "mock_access_token",
        "refresh_token": "mock_refresh_token",
        "id_token": "mock.id.token",
    }
    mock_id_token_payload = {
        "email": "newuser@icloud.com",
        "email_verified": True,
    }

    with patch("httpx.post") as mock_post, \
         patch("jwt.decode") as mock_jwt_decode, \
         patch("app.services.auth._generate_apple_client_secret") as mock_secret:

        mock_post.return_value.json.return_value = mock_apple_token_response
        mock_jwt_decode.return_value = mock_id_token_payload
        mock_secret.return_value = "mock_client_secret"

        # when
        response = client.post("/api/auth/apple", data={"code": "mock_auth_code"})

        # then
        assert response.status_code == 200
        assert response.json()["access_token"].startswith("ey")
        assert response.json()["token_type"] == "Bearer"


def test_generate_apple_client_secret():
    """Apple 클라이언트 시크릿 생성 테스트 (모킹)"""
    from app.services.auth import _generate_apple_client_secret

    # given - Apple 클라이언트 시크릿 생성 함수를 모킹
    with patch('app.services.auth.jwt.encode') as mock_jwt_encode:
        mock_jwt_encode.return_value = "mocked.jwt.token"

        # when
        client_secret = _generate_apple_client_secret()

        # then
        assert client_secret == "mocked.jwt.token"
        mock_jwt_encode.assert_called_once()
