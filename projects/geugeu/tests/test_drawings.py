from datetime import UTC, datetime

from app.models import Drawing, DrawingImage, Post


def test_create_drawing(client, session, authorized_user):
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

    content = "test content"
    image_urls = [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
    ]

    # when
    response = client.post(
        "/api/drawings",
        json={
            "post_code": post.code,
            "content": content,
            "image_urls": image_urls,
        },
    )

    # then
    assert response.status_code == 200
    assert response.json()["post"]["code"] == post.code
    assert response.json()["author"]["code"] == authorized_user.code
    assert response.json()["content"] == content
    assert response.json()["image_urls"] == image_urls


def test_get_drawings(client, session, authorized_user):
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

    drawings = [
        Drawing(
            id=i,
            code=f"abcd{i}",
            post_id=post.id,
            author_id=authorized_user.id,
            content="test content",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        for i in range(1, 4)
    ]
    session.add_all(drawings)

    # when
    response = client.get("/api/drawings")

    # then
    assert response.status_code == 200
    assert response.json()["count"] == 3
    assert len(response.json()["items"]) == 3


def test_get_drawing(client, session, authorized_user):
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

    drawing = Drawing(
        id=1,
        code="abcd123",
        post_id=post.id,
        author_id=authorized_user.id,
        content="test content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    session.add(drawing)

    drawing_images = [
        DrawingImage(
            id=i,
            code=f"abcd{i}",
            drawing_id=drawing.id,
            image_url=f"https://example.com/image{i}.jpg",
        )
        for i in range(1, 4)
    ]
    session.add_all(drawing_images)

    # when
    response = client.get(f"/api/drawings/{drawing.code}")

    # then
    assert response.status_code == 200
    assert response.json()["code"] == drawing.code
    assert response.json()["post"]["code"] == post.code
    assert response.json()["author"]["code"] == authorized_user.code
    assert response.json()["content"] == drawing.content
    assert len(response.json()["image_urls"]) == 3
