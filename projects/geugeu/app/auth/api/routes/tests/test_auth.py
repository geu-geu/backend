from unittest.mock import patch

from fastapi.testclient import TestClient

from app.auth.domain.token import Token
from app.auth.services.auth_service import AuthService
from app.main import app

client = TestClient(app)


@patch.object(AuthService, "login")
def test_login(login):
    # given
    payload = {"username": "user@example.com", "password": "P@ssw0rd1234"}

    token = Token(
        access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        token_type="Bearer",
    )
    login.return_value = token

    # when
    response = client.post("/api/auth/login", data=payload)

    # then
    assert response.status_code == 200
    assert response.json()["access_token"] == token.access_token
    assert response.json()["token_type"] == token.token_type
