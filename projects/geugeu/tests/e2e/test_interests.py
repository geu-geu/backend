import pytest

from app.core.security import get_password_hash
from app.models import Interest, Post, User


@pytest.fixture()
def post(db, user):
    post = Post(
        author_id=user.id,
        title="Test Post",
        content="Test content for interest testing",
    )
    db.add(post)
    db.flush()
    return post


@pytest.fixture()
def another_user(db):
    user = User(
        email="another@example.com",
        password=get_password_hash("P@ssw0rd1234"),
        nickname="another_user",
        is_admin=False,
        profile_image_url="",
    )
    db.add(user)
    db.flush()
    return user


def test_add_interest(client, authorized_user, post):
    # when
    response = client.post(f"/api/posts/{post.code}/interests")

    # then
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "Interest added successfully"
    assert response.json()["is_interested"] is True


def test_remove_interest(client, db, authorized_user, post):
    # given - user already has interest
    interest = Interest(user_id=authorized_user.id, post_id=post.id)
    db.add(interest)
    db.flush()

    # when
    response = client.post(f"/api/posts/{post.code}/interests")

    # then
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "Interest removed successfully"
    assert response.json()["is_interested"] is False


def test_toggle_interest_post_not_found(client, authorized_user):
    # when
    response = client.post("/api/posts/nonexistent_code/interests")

    # then
    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found"


def test_toggle_interest_unauthorized(client, post):
    # when
    response = client.post(f"/api/posts/{post.code}/interests")

    # then
    assert response.status_code == 401


def test_get_post_interests(client, db, post, user, another_user):
    # given - two users interested in the post
    interests = [
        Interest(user_id=user.id, post_id=post.id),
        Interest(user_id=another_user.id, post_id=post.id),
    ]
    db.add_all(interests)
    db.flush()

    # when
    response = client.get(f"/api/posts/{post.code}/interests")

    # then
    assert response.status_code == 200
    assert response.json()["count"] == 2
    assert len(response.json()["items"]) == 2
    assert "is_interested" not in response.json()  # not authenticated

    # Check first interest
    first_interest = response.json()["items"][0]
    assert "code" in first_interest
    assert first_interest["user"]["email"] in [
        "user@example.com",
        "another@example.com",
    ]
    assert first_interest["post"]["code"] == post.code
    assert first_interest["post"]["title"] == post.title


def test_get_post_interests_with_auth(client, db, authorized_user, post):
    # given - current user has interest
    interest = Interest(user_id=authorized_user.id, post_id=post.id)
    db.add(interest)
    db.flush()

    # when
    response = client.get(f"/api/posts/{post.code}/interests")

    # then
    assert response.status_code == 200
    assert response.json()["count"] == 1
    assert response.json()["is_interested"] is True  # authenticated and interested


def test_get_post_interests_with_auth_not_interested(
    client, db, authorized_user, post, another_user
):
    # given - another user has interest, but not the current user
    interest = Interest(user_id=another_user.id, post_id=post.id)
    db.add(interest)
    db.flush()

    # when
    response = client.get(f"/api/posts/{post.code}/interests")

    # then
    assert response.status_code == 200
    assert response.json()["count"] == 1
    assert response.json()["is_interested"] is False  # authenticated but not interested


def test_get_post_interests_summary_only(client, db, post, user, another_user):
    # given - two users interested in the post
    interests = [
        Interest(user_id=user.id, post_id=post.id),
        Interest(user_id=another_user.id, post_id=post.id),
    ]
    db.add_all(interests)
    db.flush()

    # when - request with page_size=0 for summary only
    response = client.get(f"/api/posts/{post.code}/interests?page_size=0")

    # then
    assert response.status_code == 200
    assert response.json()["count"] == 2
    assert response.json()["items"] == []  # no user details
    assert "is_interested" not in response.json()  # not authenticated


def test_get_post_interests_pagination(client, db, post):
    # given - create 25 users with interests
    users = []
    interests = []
    for i in range(25):
        user = User(
            email=f"user{i}@example.com",
            password=get_password_hash("P@ssw0rd1234"),
            nickname=f"user{i}",
            is_admin=False,
            profile_image_url="",
        )
        users.append(user)
    db.add_all(users)
    db.flush()

    for user in users:
        interest = Interest(user_id=user.id, post_id=post.id)
        interests.append(interest)
    db.add_all(interests)
    db.flush()

    # when - get first page
    response = client.get(f"/api/posts/{post.code}/interests?page=1&page_size=10")

    # then
    assert response.status_code == 200
    assert response.json()["count"] == 25
    assert len(response.json()["items"]) == 10

    # when - get second page
    response = client.get(f"/api/posts/{post.code}/interests?page=2&page_size=10")

    # then
    assert response.status_code == 200
    assert response.json()["count"] == 25
    assert len(response.json()["items"]) == 10


def test_get_user_interests(client, db, user, another_user):
    # given - user interested in multiple posts
    posts = []
    interests = []
    for i in range(3):
        post = Post(
            author_id=another_user.id,
            title=f"Post {i}",
            content=f"Content {i}",
        )
        posts.append(post)
    db.add_all(posts)
    db.flush()

    for post in posts:
        interest = Interest(user_id=user.id, post_id=post.id)
        interests.append(interest)
    db.add_all(interests)
    db.flush()

    # when
    response = client.get(f"/api/users/{user.code}/interests")

    # then
    assert response.status_code == 200
    assert response.json()["count"] == 3
    assert len(response.json()["items"]) == 3

    # Check structure
    first_interest = response.json()["items"][0]
    assert first_interest["user"]["code"] == user.code
    assert "post" in first_interest
    assert "created_at" in first_interest


def test_get_user_interests_user_not_found(client):
    # when
    response = client.get("/api/users/nonexistent_code/interests")

    # then
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_soft_delete_interest(client, db, authorized_user, post):
    # given - user has interest
    interest = Interest(user_id=authorized_user.id, post_id=post.id)
    db.add(interest)
    db.flush()

    # when - toggle interest (soft delete)
    response = client.post(f"/api/posts/{post.code}/interests")
    assert response.status_code == 200
    assert response.json()["is_interested"] is False

    # then - verify count doesn't include soft deleted
    response = client.get(f"/api/posts/{post.code}/interests?page_size=0")
    assert response.json()["count"] == 0

    # when - toggle again (new interest)
    response = client.post(f"/api/posts/{post.code}/interests")
    assert response.status_code == 200
    assert response.json()["is_interested"] is True

    # then - verify count is 1
    response = client.get(f"/api/posts/{post.code}/interests?page_size=0")
    assert response.json()["count"] == 1
