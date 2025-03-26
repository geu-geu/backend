from datetime import UTC, datetime
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from ulid import ULID

from app.auth.dependencies import get_current_active_user
from app.main import app
from app.post.application.post_service import PostService
from app.post.domain.post import Post
from app.post.domain.post_image import PostImage
from app.user.domain.user import User

client = TestClient(app)


@pytest.fixture(autouse=True)
def override_auth_dependency():
    def override_current_active_user_dep():
        return User(
            id=str(ULID()),
            email="user@example.com",
            name=None,
            password="password",
            is_admin=False,
            is_active=True,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

    app.dependency_overrides[get_current_active_user] = override_current_active_user_dep


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
