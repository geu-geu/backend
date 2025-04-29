from datetime import UTC, datetime

from app.models import Post


def test_create_post(client, authorized_user):
    # given
    title = "test title"
    content = "test content"

    # when
    response = client.post("/api/posts", json={"title": title, "content": content})

    # then
    assert response.status_code == 201
    assert response.json()["title"] == title
    assert response.json()["content"] == content


def test_get_posts(client, session, authorized_user):
    # given
    posts = [
        Post(
            id=i,
            code=f"abcd{i}",
            author_id=authorized_user.id,
            title="test title",
            content="test content",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        for i in range(1, 4)
    ]
    session.add_all(posts)

    # when
    response = client.get("/api/posts")

    # then
    assert response.status_code == 200
    assert response.json()["count"] == 3
    assert len(response.json()["items"]) == 3


def test_get_post(client, session, authorized_user):
    # given
    post = Post(
        id=1,
        code="abcd123",
        author_id=authorized_user.id,
        title="test title",
        content="test content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    session.add(post)

    # when
    response = client.get(f"/api/posts/{post.code}")

    # then
    assert response.status_code == 200
    assert response.json()["title"] == post.title
    assert response.json()["content"] == post.content


def test_update_post(client, session, authorized_user):
    # given
    post = Post(
        id=1,
        code="abcd123",
        author_id=authorized_user.id,
        title="test title",
        content="test content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    session.add(post)

    new_title = "new title"

    # when
    response = client.put(f"/api/posts/{post.code}", json={"title": new_title})

    # then
    assert response.status_code == 200
    assert response.json()["title"] == new_title


def test_delete_post(client, session, authorized_user):
    # given
    post = Post(
        id=1,
        code="abcd123",
        author_id=authorized_user.id,
        title="test title",
        content="test content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    session.add(post)

    # when
    response = client.delete(f"/api/posts/{post.code}")

    # then
    assert response.status_code == 204
    session.refresh(post)
    assert post.is_deleted
