from app.models import Drawing, DrawingImage, Post


def test_create_drawing(client, session, authorized_user):
    # given
    post = Post(
        code="abcd123",
        author_id=authorized_user.id,
        title="test title",
        content="test content",
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
    assert response.status_code == 201
    assert response.json()["post"]["code"] == post.code
    assert response.json()["author"]["code"] == authorized_user.code
    assert response.json()["content"] == content
    assert response.json()["image_urls"] == image_urls


def test_create_drawing_twice_fails(client, session, authorized_user):
    # given
    post = Post(
        code="abcd123",
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    drawing = Drawing(
        code="abcd123",
        post_id=post.id,
        author_id=authorized_user.id,
        content="test content",
    )
    session.add(drawing)
    session.flush()

    # when
    response = client.post(
        "/api/drawings",
        json={
            "post_code": post.code,
            "content": "test content",
            "image_urls": ["https://example.com/image.jpg"],
        },
    )

    # then
    assert response.status_code == 400
    assert response.json()["detail"] == "Drawing already exists"


def test_get_drawings(client, session, authorized_user):
    # given
    post = Post(
        code="abcd123",
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    drawings = [
        Drawing(
            code=f"abcd{i}",
            post_id=post.id,
            author_id=authorized_user.id,
            content="test content",
        )
        for i in range(1, 4)
    ]
    session.add_all(drawings)
    session.flush()

    # when
    response = client.get("/api/drawings")

    # then
    assert response.status_code == 200
    assert response.json()["count"] == 3
    assert len(response.json()["items"]) == 3


def test_get_drawing(client, session, authorized_user):
    # given
    post = Post(
        code="abcd123",
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    drawing = Drawing(
        code="abcd123",
        post_id=post.id,
        author_id=authorized_user.id,
        content="test content",
    )
    session.add(drawing)
    session.flush()

    drawing_images = [
        DrawingImage(
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
        code="abcd123",
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    drawing = Drawing(
        code="abcd123",
        post_id=post.id,
        author_id=authorized_user.id,
        content="test content",
    )
    session.add(drawing)
    session.flush()

    drawing_images = [
        DrawingImage(
            code=f"abcd{i}",
            drawing_id=drawing.id,
            image_url=f"https://example.com/image{i}.jpg",
        )
        for i in range(1, 4)
    ]
    session.add_all(drawing_images)

    new_content = "new content"
    new_image_urls = [
        "https://example.com/new1.jpg",
        "https://example.com/new2.jpg",
    ]

    # when
    response = client.put(
        f"/api/drawings/{drawing.code}",
        json={
            "content": new_content,
            "image_urls": new_image_urls,
        },
    )

    # then
    assert response.status_code == 200
    assert response.json()["code"] == drawing.code
    assert response.json()["post"]["code"] == post.code
    assert response.json()["author"]["code"] == authorized_user.code
    assert response.json()["content"] == new_content
    assert len(response.json()["image_urls"]) == 2


def test_update_drawing_404(client, authorized_user):
    # given
    code = "abcd123"

    # when
    response = client.put(
        f"/api/drawings/{code}",
        json={
            "content": "new content",
            "image_urls": ["http://example.com/image.png"],
        },
    )

    # then
    assert response.status_code == 404


def test_delete_drawing(client, session, authorized_user):
    # given
    post = Post(
        code="abcd123",
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    drawing = Drawing(
        code="abcd123",
        post_id=post.id,
        author_id=authorized_user.id,
        content="test content",
    )
    session.add(drawing)
    session.flush()

    drawing_images = [
        DrawingImage(
            code=f"abcd{i}",
            drawing_id=drawing.id,
            image_url=f"https://example.com/image{i}.jpg",
        )
        for i in range(1, 4)
    ]
    session.add_all(drawing_images)

    assert drawing.deleted_at is None

    # when
    response = client.delete(f"/api/drawings/{drawing.code}")

    # then
    assert response.status_code == 204
    session.refresh(drawing)
    assert drawing.deleted_at is not None


def test_delete_drawing_404(client, authorized_user):
    # given
    code = "abcd123"

    # when
    response = client.delete(f"/api/drawings/{code}")

    # then
    assert response.status_code == 404
