def test_create_user(client):
    # given
    email = "user@example.com"
    password = "P@ssw0rd1234"

    # when
    response = client.post("/api/users", json={"email": email, "password": password})

    # then
    assert response.status_code == 201
    assert response.json()["email"] == email


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


def test_update_me(client, authorized_user):
    # given
    new_nickname = "geugeugood"

    # when
    response = client.put("/api/users/me", json={"nickname": new_nickname})

    # then
    assert response.status_code == 200
    assert response.json()["nickname"] == new_nickname


def test_delete_me(client, session, authorized_user):
    # when
    response = client.delete("/api/users/me")

    # then
    assert response.status_code == 204
    session.refresh(authorized_user)
    assert authorized_user.is_active is False
