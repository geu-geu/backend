def test_create_user(client):
    # given
    email = "user@example.com"
    password = "P@ssw0rd1234"

    # when
    response = client.post("/api/users", json={"email": email, "password": password})

    # then
    assert response.status_code == 201
    assert response.json()["email"] == email
