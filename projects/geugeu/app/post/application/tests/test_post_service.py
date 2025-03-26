from datetime import UTC, datetime
from typing import Any

import pytest
from pytest_mock import MockerFixture
from ulid import ULID

from app.post.application.post_service import PostService
from app.post.domain.post import Post
from app.post.domain.post_image import PostImage
from app.post.domain.post_image_repository import IPostImageRepository
from app.post.domain.post_repository import IPostRepository


@pytest.fixture()
def post_repository(mocker: MockerFixture) -> Any:
    return mocker.Mock(spec=IPostRepository)


@pytest.fixture()
def post_image_repository(mocker: MockerFixture) -> Any:
    return mocker.Mock(spec=IPostImageRepository)


@pytest.fixture()
def post_service(
    post_repository: IPostRepository,
    post_image_repository: IPostImageRepository,
) -> PostService:
    return PostService(
        post_repository=post_repository,
        post_image_repository=post_image_repository,
    )


def test_create_post(post_service: PostService) -> None:
    # given
    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title="title",
        content="content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    image_urls = ["https://example.com/image1.png", "https://example.com/image2.png"]

    post_service.post_repository.save.return_value = post
    post_service.post_image_repository.save.return_value = [
        PostImage(
            id=str(ULID()),
            post_id=post.id,
            image_url=image_url,
        )
        for image_url in image_urls
    ]

    # when
    post, images = post_service.create_post(post, image_urls)

    # then
    assert post.id == post.id
    assert post.author_id == post.author_id
    assert post.title == post.title
    assert post.content == post.content
    assert post.created_at == post.created_at
    assert post.updated_at == post.updated_at
    assert len(images) == len(image_urls)
    for image in images:
        assert image.post_id == post.id
        assert image.image_url in image_urls


def test_get_post(post_service: PostService) -> None:
    # given
    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title="title",
        content="content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_service.post_repository.find_by_id.return_value = post

    # when
    result = post_service.get_post(post.id)

    # then
    assert result.id == post.id
    assert result.author_id == post.author_id
    assert result.title == post.title
    assert result.content == post.content
