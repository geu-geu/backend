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
