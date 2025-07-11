import io

from app.core.security import get_password_hash
from app.models import Image, Post, User


def test_create_post(client, authorized_user):
    # given
    title = "test title"
    content = "test content"

    # when
    response = client.post(
        "/api/posts",
        data={"title": title, "content": content},
        files=[
            ("files", ("test.png", io.BytesIO(b"imagebytes"), "image/png")),
        ],
    )

    # then
    assert response.status_code == 201
    assert response.json()["title"] == title
    assert response.json()["content"] == content
    assert len(response.json()["images"]) == 1


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


def test_get_posts(client, db, authorized_user):
    # given
    posts = [
        Post(
            author_id=authorized_user.id,
            title="test title",
            content="test content",
        )
        for _ in range(3)
    ]
    db.add_all(posts)
    db.flush()

    # when
    response = client.get("/api/posts")

    # then
    assert response.status_code == 200
    assert response.json()["count"] == 3
    assert len(response.json()["items"]) == 3


def test_get_posts_with_author_code(client, db, authorized_user):
    # given
    other_user = User(
        email="other@example.com",
        password=get_password_hash("P@ssw0rd1234"),
        nickname="other",
        is_admin=False,
        profile_image_url="",
    )
    db.add(other_user)
    db.flush()

    post1 = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    db.add(post1)
    db.flush()

    post2 = Post(
        author_id=other_user.id,
        title="test title",
        content="test content",
    )
    db.add(post2)
    db.flush()

    # when
    response = client.get(f"/api/posts?author_code={authorized_user.code}")

    # then
    assert response.status_code == 200
    assert response.json()["count"] == 1
    assert len(response.json()["items"]) == 1
    assert response.json()["items"][0]["author"]["code"] == authorized_user.code


def test_get_posts_401(client, user):
    # when
    response = client.get("/api/posts")

    # then
    assert response.status_code == 401


def test_get_post(client, db, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    db.add(post)
    db.flush()

    images = [
        Image(
            post_id=post.id,
            url="https://example.com/image.jpg",
        )
        for _ in range(3)
    ]
    db.add_all(images)
    db.flush()

    # when
    response = client.get(f"/api/posts/{post.code}")

    # then
    assert response.status_code == 200
    assert response.json()["title"] == post.title
    assert response.json()["content"] == post.content
    assert len(response.json()["images"]) == len(images)


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


def test_update_post(client, db, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    db.add(post)
    db.flush()

    post_images = [
        Image(
            post_id=post.id,
            url=f"https://example.com/image{i}.jpg",
        )
        for i in range(1, 4)
    ]
    db.add_all(post_images)

    # when
    response = client.put(
        f"/api/posts/{post.code}",
        data={
            "title": "new title",
            "content": "new content",
        },
        files=[
            ("files", ("test1.png", io.BytesIO(b"imagebytes"), "image/png")),
            ("files", ("test2.png", io.BytesIO(b"imagebytes"), "image/png")),
        ],
    )

    # then
    assert response.status_code == 200
    assert response.json()["title"] == "new title"
    assert response.json()["content"] == "new content"
    assert len(response.json()["images"]) == 2


def test_update_post_403(client, db, authorized_user, hashed_password):
    # given
    author = User(
        email="test@example.com",
        password=hashed_password,
    )
    db.add(author)
    db.flush()

    post = Post(
        author_id=author.id,
        title="test title",
        content="test content",
    )
    db.add(post)
    db.flush()

    # when
    response = client.put(
        f"/api/posts/{post.code}",
        data={
            "title": "new title",
            "content": "new content",
        },
        files=[
            ("files", ("test1.png", io.BytesIO(b"imagebytes"), "image/png")),
            ("files", ("test2.png", io.BytesIO(b"imagebytes"), "image/png")),
        ],
    )

    # then
    assert response.status_code == 403


def test_update_post_by_admin(client, db, authorized_user, hashed_password):
    # given
    author = User(
        email="test@example.com",
        password=hashed_password,
    )
    db.add(author)
    db.flush()

    post = Post(
        author_id=author.id,
        title="test title",
        content="test content",
    )
    db.add(post)
    db.flush()

    authorized_user.is_admin = True

    # when
    response = client.put(
        f"/api/posts/{post.code}",
        data={
            "title": "new title",
            "content": "new content",
        },
        files=[
            ("files", ("test1.png", io.BytesIO(b"imagebytes"), "image/png")),
            ("files", ("test2.png", io.BytesIO(b"imagebytes"), "image/png")),
        ],
    )

    # then
    assert response.status_code == 200


def test_update_post_401(client, user):
    # when
    response = client.put(
        "/api/posts/abcd123",
        data={
            "title": "new title",
            "content": "new content",
        },
        files=[
            ("files", ("test1.png", io.BytesIO(b"imagebytes"), "image/png")),
            ("files", ("test2.png", io.BytesIO(b"imagebytes"), "image/png")),
        ],
    )

    # then
    assert response.status_code == 401


def test_update_post_404(client, authorized_user):
    # given
    code = "abcd123"

    # when
    response = client.put(
        f"/api/posts/{code}",
        data={
            "title": "new title",
            "content": "new content",
        },
        files=[
            ("files", ("test1.png", io.BytesIO(b"imagebytes"), "image/png")),
            ("files", ("test2.png", io.BytesIO(b"imagebytes"), "image/png")),
        ],
    )

    # then
    assert response.status_code == 404


def test_delete_post(client, db, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    db.add(post)
    db.flush()

    assert post.deleted_at is None

    # when
    response = client.delete(f"/api/posts/{post.code}")

    # then
    assert response.status_code == 204
    db.refresh(post)
    assert post.deleted_at is not None


def test_delete_post_401(client, user):
    # when
    response = client.delete("/api/posts/abcd123")

    # then
    assert response.status_code == 401


def test_delete_post_403(client, db, authorized_user, hashed_password):
    # given
    author = User(
        email="test@example.com",
        password=hashed_password,
    )
    db.add(author)
    db.flush()

    post = Post(
        author_id=author.id,
        title="test title",
        content="test content",
    )
    db.add(post)
    db.flush()

    # when
    response = client.delete(f"/api/posts/{post.code}")

    # then
    assert response.status_code == 403


def test_delete_post_by_admin(client, db, authorized_user, hashed_password):
    # given
    author = User(
        email="test@example.com",
        password=hashed_password,
    )
    db.add(author)
    db.flush()

    post = Post(
        author_id=author.id,
        title="test title",
        content="test content",
    )
    db.add(post)
    db.flush()

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
