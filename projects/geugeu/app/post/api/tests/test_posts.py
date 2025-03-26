from datetime import UTC, datetime
from unittest.mock import patch

from fastapi.testclient import TestClient
from ulid import ULID

from app.main import app
from app.post.application.post_service import PostService
from app.post.domain.post import Post
from app.post.domain.post_image import PostImage

client = TestClient(app)


@patch.object(PostService, "create_post")
def test_create_post(create_post):
    # given
    title = "title"
    content = "content"
    image_urls = [
        "https://example.com/image1.png",
        "https://example.com/image2.png",
    ]

    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title=title,
        content=content,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    images = [
        PostImage(
            id=str(ULID()),
            post_id=post.id,
            image_url=image_url,
        )
        for image_url in image_urls
    ]
    create_post.return_value = post, images

    # when
    response = client.post(
        "/api/posts",
        json={"title": title, "content": content, "image_urls": image_urls},
    )

    # then
    assert response.status_code == 201
    assert response.json()["id"] == post.id
    assert response.json()["title"] == post.title
    assert response.json()["content"] == post.content
    assert response.json()["images"] == [image.image_url for image in images]


@patch.object(PostService, "get_post")
def test_get_post(get_post):
    # given
    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title="title",
        content="content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    images = [
        PostImage(
            id=str(ULID()),
            post_id=post.id,
            image_url="https://example.com/image1.png",
        ),
        PostImage(
            id=str(ULID()),
            post_id=post.id,
            image_url="https://example.com/image2.png",
        ),
    ]
    get_post.return_value = post, images

    # when
    response = client.get(f"/api/posts/{post.id}")

    # then
    assert response.status_code == 200
    assert response.json()["id"] == post.id
    assert response.json()["title"] == post.title
    assert response.json()["content"] == post.content
    assert response.json()["images"] == [image.image_url for image in images]


@patch.object(PostService, "update_post")
def test_update_post(update_post):
    # given
    post_id = str(ULID())
    updated_title = "updated title"
    updated_content = "updated content"
    updated_image_urls = [
        "https://example.com/updated_image1.png",
        "https://example.com/updated_image2.png",
    ]

    updated_post = Post(
        id=post_id,
        author_id=str(ULID()),
        title=updated_title,
        content=updated_content,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    updated_images = [
        PostImage(
            id=str(ULID()),
            post_id=post_id,
            image_url=image_url,
        )
        for image_url in updated_image_urls
    ]
    update_post.return_value = updated_post, updated_images

    # when
    response = client.put(
        f"/api/posts/{post_id}",
        json={
            "title": updated_title,
            "content": updated_content,
            "image_urls": updated_image_urls,
        },
    )

    # then
    assert response.status_code == 200
    assert response.json()["id"] == updated_post.id
    assert response.json()["title"] == updated_post.title
    assert response.json()["content"] == updated_post.content
    assert response.json()["images"] == [image.image_url for image in updated_images]


@patch.object(PostService, "delete_post")
def test_delete_post(delete_post):
    # given
    post_id = str(ULID())
    delete_post.return_value = None

    # when
    response = client.delete(f"/api/posts/{post_id}")

    # then
    assert response.status_code == 204
    delete_post.assert_called_once_with(post_id=post_id)
