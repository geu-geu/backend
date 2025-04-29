from datetime import UTC, datetime

from app.models import Post


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
