import io
from datetime import UTC, datetime

from app.models import Drawing, Image, Post, User


def test_create_drawing(client, session, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    # when
    response = client.post(
        "/api/drawings",
        data={
            "post_code": post.code,
            "content": "test content",
        },
        files=[
            ("files", ("test1.png", io.BytesIO(b"imagebytes"), "image/png")),
            ("files", ("test2.png", io.BytesIO(b"imagebytes"), "image/png")),
        ],
    )

    # then
    assert response.status_code == 201
    assert response.json()["post"]["code"] == post.code
    assert response.json()["author"]["code"] == authorized_user.code
    assert response.json()["content"] == "test content"
    assert len(response.json()["images"]) == 2


def test_create_drawing_401(client, user):
    # when
    response = client.post(
        "/api/drawings",
        data={
            "post_code": "abcd123",
            "content": "test content",
        },
        files=[
            ("files", ("test.png", io.BytesIO(b"imagebytes"), "image/png")),
        ],
    )

    # then
    assert response.status_code == 401


def test_create_drawing_twice_fails(client, session, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    drawing = Drawing(
        post_id=post.id,
        author_id=authorized_user.id,
        content="test content",
    )
    session.add(drawing)
    session.flush()

    # when
    response = client.post(
        "/api/drawings",
        data={
            "post_code": post.code,
            "content": "test content",
        },
        files=[
            ("files", ("test.png", io.BytesIO(b"imagebytes"), "image/png")),
        ],
    )

    # then
    assert response.status_code == 400
    assert response.json()["detail"] == "Drawing already exists"


def test_get_drawings(client, session, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    drawings = [
        Drawing(
            post_id=post.id,
            author_id=authorized_user.id,
            content="test content",
        )
        for _ in range(3)
    ]
    session.add_all(drawings)
    session.flush()

    _deleted_drawings = [
        Drawing(
            post_id=post.id,
            author_id=authorized_user.id,
            content="deleted drawing",
            deleted_at=datetime.now(UTC),
        )
        for _ in range(2)
    ]
    session.add_all(_deleted_drawings)
    session.flush()

    # when
    response = client.get("/api/drawings")

    # then
    assert response.status_code == 200
    assert response.json()["count"] == 3
    assert len(response.json()["items"]) == 3


def test_get_drawings_401(client, user):
    # when
    response = client.get("/api/drawings")

    # then
    assert response.status_code == 401


def test_get_drawing(client, session, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    drawing = Drawing(
        post_id=post.id,
        author_id=authorized_user.id,
        content="test content",
    )
    session.add(drawing)
    session.flush()

    images = [
        Image(
            drawing_id=drawing.id,
            url="https://example.com/image.jpg",
        )
        for _ in range(3)
    ]
    session.add_all(images)
    session.flush()

    _deleted_images = [
        Image(
            drawing_id=drawing.id,
            url="https://example.com/image.jpg",
            deleted_at=datetime.now(UTC),
        )
        for _ in range(2)
    ]
    session.add_all(_deleted_images)
    session.flush()

    # when
    response = client.get(f"/api/drawings/{drawing.code}")

    # then
    assert response.status_code == 200
    assert response.json()["code"] == drawing.code
    assert response.json()["post"]["code"] == post.code
    assert response.json()["author"]["code"] == authorized_user.code
    assert response.json()["content"] == drawing.content
    assert len(response.json()["images"]) == 3


def test_get_drawing_401(client, user):
    # when
    response = client.get("/api/drawings/abcd123")

    # then
    assert response.status_code == 401


def test_get_drawing_404(client, authorized_user):
    # given
    code = "abcd123"

    # when
    response = client.get(f"/api/drawings/{code}")

    # then
    assert response.status_code == 404


def test_update_drawing(client, session, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    drawing = Drawing(
        post_id=post.id,
        author_id=authorized_user.id,
        content="test content",
    )
    session.add(drawing)
    session.flush()

    images = [
        Image(
            drawing_id=drawing.id,
            url="https://example.com/image.jpg",
        )
        for _ in range(3)
    ]
    session.add_all(images)
    session.flush()

    # when
    response = client.put(
        f"/api/drawings/{drawing.code}",
        data={
            "content": "new content",
        },
        files=[
            ("files", ("test1.png", io.BytesIO(b"imagebytes"), "image/png")),
            ("files", ("test2.png", io.BytesIO(b"imagebytes"), "image/png")),
        ],
    )

    # then
    assert response.status_code == 200
    assert response.json()["code"] == drawing.code
    assert response.json()["post"]["code"] == post.code
    assert response.json()["author"]["code"] == authorized_user.code
    assert response.json()["content"] == "new content"
    assert len(response.json()["images"]) == 2


def test_update_drawing_401(client, user):
    # when
    response = client.put(
        "/api/drawings/abcd123",
        data={
            "content": "new content",
        },
        files=[
            ("files", ("test.png", io.BytesIO(b"imagebytes"), "image/png")),
        ],
    )

    # then
    assert response.status_code == 401


def test_update_drawing_403(client, session, authorized_user, hashed_password):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    author = User(
        email="test@example.com",
        password=hashed_password,
    )
    session.add(author)
    session.flush()

    drawing = Drawing(
        post_id=post.id,
        author_id=author.id,
        content="test content",
    )
    session.add(drawing)
    session.flush()

    # when
    response = client.put(
        f"/api/drawings/{drawing.code}",
        data={
            "content": "new content",
        },
        files=[
            ("files", ("test.png", io.BytesIO(b"imagebytes"), "image/png")),
        ],
    )

    # then
    assert response.status_code == 403


def test_update_drawing_by_admin(client, session, authorized_user, hashed_password):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    author = User(
        email="test@example.com",
        password=hashed_password,
    )
    session.add(author)
    session.flush()

    drawing = Drawing(
        post_id=post.id,
        author_id=author.id,
        content="test content",
    )
    session.add(drawing)
    session.flush()

    authorized_user.is_admin = True

    # when
    response = client.put(
        f"/api/drawings/{drawing.code}",
        data={
            "content": "new content",
        },
        files=[
            ("files", ("test.png", io.BytesIO(b"imagebytes"), "image/png")),
        ],
    )

    # then
    assert response.status_code == 200


def test_update_drawing_404(client, authorized_user):
    # given
    code = "abcd123"

    # when
    response = client.put(
        f"/api/drawings/{code}",
        data={
            "content": "new content",
        },
        files=[
            ("files", ("test.png", io.BytesIO(b"imagebytes"), "image/png")),
        ],
    )

    # then
    assert response.status_code == 404


def test_delete_drawing(client, session, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    drawing = Drawing(
        post_id=post.id,
        author_id=authorized_user.id,
        content="test content",
    )
    session.add(drawing)
    session.flush()

    images = [
        Image(
            drawing_id=drawing.id,
            url="https://example.com/image.jpg",
        )
        for _ in range(3)
    ]
    session.add_all(images)
    session.flush()

    assert drawing.deleted_at is None

    # when
    response = client.delete(f"/api/drawings/{drawing.code}")

    # then
    assert response.status_code == 204
    session.refresh(drawing)
    assert drawing.deleted_at is not None


def test_delete_drawing_401(client, user):
    # when
    response = client.delete("/api/drawings/abcd123")

    # then
    assert response.status_code == 401


def test_delete_drawing_403(client, session, authorized_user, hashed_password):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    author = User(
        email="test@example.com",
        password=hashed_password,
    )
    session.add(author)
    session.flush()

    drawing = Drawing(
        post_id=post.id,
        author_id=author.id,
        content="test content",
    )
    session.add(drawing)
    session.flush()

    # when
    response = client.delete(f"/api/drawings/{drawing.code}")

    # then
    assert response.status_code == 403


def test_delete_drawing_by_admin(client, session, authorized_user, hashed_password):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    author = User(
        email="test@example.com",
        password=hashed_password,
    )
    session.add(author)
    session.flush()

    drawing = Drawing(
        post_id=post.id,
        author_id=author.id,
        content="test content",
    )
    session.add(drawing)
    session.flush()

    authorized_user.is_admin = True

    # when
    response = client.delete(f"/api/drawings/{drawing.code}")

    # then
    assert response.status_code == 204


def test_delete_drawing_404(client, authorized_user):
    # given
    code = "abcd123"

    # when
    response = client.delete(f"/api/drawings/{code}")

    # then
    assert response.status_code == 404
