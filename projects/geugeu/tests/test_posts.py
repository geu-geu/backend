from app.models import Image, Post, User


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


def test_create_post_401(client, user):
    # when
    response = client.post(
        "/api/posts",
        json={
            "title": "test title",
            "content": "test content",
        },
    )

    # then
    assert response.status_code == 401


def test_get_posts(client, session, authorized_user):
    # given
    posts = [
        Post(
            code=f"abcd{i}",
            author_id=authorized_user.id,
            title="test title",
            content="test content",
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


def test_get_posts_401(client, user):
    # when
    response = client.get("/api/posts")

    # then
    assert response.status_code == 401


def test_get_post(client, session, authorized_user):
    # given
    post = Post(
        code="abcd123",
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    images = [
        Image(
            code=f"abcd{i}",
            post_id=post.id,
            url=f"https://example.com/image{i}.jpg",
        )
        for i in range(1, 4)
    ]
    session.add_all(images)

    # when
    response = client.get(f"/api/posts/{post.code}")

    # then
    assert response.status_code == 200
    assert response.json()["title"] == post.title
    assert response.json()["content"] == post.content
    assert len(response.json()["image_urls"]) == len(images)


def test_get_post_401(client, user):
    # when
    response = client.get("/api/posts/abcd123")

    # then
    assert response.status_code == 401


def test_get_post_404(client, authorized_user):
    # given
    code = "abcd123"

    # when
    response = client.get(f"/api/posts/{code}")

    # then
    assert response.status_code == 404


def test_update_post(client, session, authorized_user):
    # given
    post = Post(
        code="abcd123",
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    post_images = [
        Image(
            code=f"abcd{i}",
            post_id=post.id,
            url=f"https://example.com/image{i}.jpg",
        )
        for i in range(1, 4)
    ]
    session.add_all(post_images)

    new_title = "new title"
    new_content = "new content"
    new_image_urls = [
        "https://example.com/new1.jpg",
        "https://example.com/new2.jpg",
    ]

    # when
    response = client.put(
        f"/api/posts/{post.code}",
        json={
            "title": new_title,
            "content": new_content,
            "image_urls": new_image_urls,
        },
    )

    # then
    assert response.status_code == 200
    assert response.json()["title"] == new_title
    assert response.json()["content"] == new_content
    assert len(response.json()["image_urls"]) == len(new_image_urls)


def test_update_post_403(client, session, authorized_user, hashed_password):
    # given
    author = User(
        code="abcd124",
        email="test@example.com",
        password=hashed_password,
    )
    session.add(author)
    session.flush()

    post = Post(
        code="abcd123",
        author_id=author.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    # when
    response = client.put(
        f"/api/posts/{post.code}",
        json={
            "title": "new title",
            "content": "new content",
            "image_urls": ["http://example.com/image.png"],
        },
    )

    # then
    assert response.status_code == 403


def test_update_post_by_admin(client, session, authorized_user, hashed_password):
    # given
    author = User(
        code="abcd124",
        email="test@example.com",
        password=hashed_password,
    )
    session.add(author)
    session.flush()

    post = Post(
        code="abcd123",
        author_id=author.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    authorized_user.is_admin = True

    # when
    response = client.put(
        f"/api/posts/{post.code}",
        json={
            "title": "new title",
            "content": "new content",
            "image_urls": ["http://example.com/image.png"],
        },
    )

    # then
    assert response.status_code == 200


def test_update_post_401(client, user):
    # when
    response = client.put(
        "/api/posts/abcd123",
        json={
            "title": "new title",
            "content": "new content",
        },
    )

    # then
    assert response.status_code == 401


def test_update_post_404(client, authorized_user):
    # given
    code = "abcd123"

    # when
    response = client.put(
        f"/api/posts/{code}",
        json={
            "title": "new title",
            "content": "new content",
            "image_urls": ["http://example.com/image.png"],
        },
    )

    # then
    assert response.status_code == 404


def test_delete_post(client, session, authorized_user):
    # given
    post = Post(
        code="abcd123",
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    assert post.deleted_at is None

    # when
    response = client.delete(f"/api/posts/{post.code}")

    # then
    assert response.status_code == 204
    session.refresh(post)
    assert post.deleted_at is not None


def test_delete_post_401(client, user):
    # when
    response = client.delete("/api/posts/abcd123")

    # then
    assert response.status_code == 401


def test_delete_post_403(client, session, authorized_user, hashed_password):
    # given
    author = User(
        code="abcd124",
        email="test@example.com",
        password=hashed_password,
    )
    session.add(author)
    session.flush()

    post = Post(
        code="abcd123",
        author_id=author.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    # when
    response = client.delete(f"/api/posts/{post.code}")

    # then
    assert response.status_code == 403


def test_delete_post_by_admin(client, session, authorized_user, hashed_password):
    # given
    author = User(
        code="abcd124",
        email="test@example.com",
        password=hashed_password,
    )
    session.add(author)
    session.flush()

    post = Post(
        code="abcd123",
        author_id=author.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    authorized_user.is_admin = True

    # when
    response = client.delete(f"/api/posts/{post.code}")

    # then
    assert response.status_code == 204


def test_delete_post_404(client, authorized_user):
    # given
    code = "abcd123"

    # when
    response = client.delete(f"/api/posts/{code}")

    # then
    assert response.status_code == 404
