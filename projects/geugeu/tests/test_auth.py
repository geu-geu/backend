from datetime import UTC, datetime


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


def test_login_with_deleted_email(client, session, user, raw_password):
    # given
    user.deleted_at = datetime.now(UTC)
    session.flush()

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
