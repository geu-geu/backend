from app.models import Post, PostImage


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


def test_get_post(client, session, authorized_user):
    # given
    post = Post(
        id=1,
        code="abcd123",
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)

    post_images = [
        PostImage(
            code=f"abcd{i}",
            post_id=post.id,
            image_url=f"https://example.com/image{i}.jpg",
        )
        for i in range(1, 4)
    ]
    session.add_all(post_images)

    # when
    response = client.get(f"/api/posts/{post.code}")

    # then
    assert response.status_code == 200
    assert response.json()["title"] == post.title
    assert response.json()["content"] == post.content
    assert len(response.json()["image_urls"]) == len(post_images)


def test_update_post(client, session, authorized_user):
    # given
    post = Post(
        id=1,
        code="abcd123",
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)

    post_images = [
        PostImage(
            code=f"abcd{i}",
            post_id=post.id,
            image_url=f"https://example.com/image{i}.jpg",
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


def test_delete_post(client, session, authorized_user):
    # given
    post = Post(
        id=1,
        code="abcd123",
        author_id=authorized_user.id,
        title="test title",
        content="test content",
        is_deleted=False,
    )
    session.add(post)

    # when
    response = client.delete(f"/api/posts/{post.code}")

    # then
    assert response.status_code == 204
    session.refresh(post)
    assert post.is_deleted
