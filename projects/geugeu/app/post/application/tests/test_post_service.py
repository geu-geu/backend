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
    result_post, result_images = post_service.create_post(post, image_urls)

    # then
    assert result_post.id == post.id
    assert result_post.author_id == post.author_id
    assert result_post.title == post.title
    assert result_post.content == post.content
    assert result_post.created_at == post.created_at
    assert result_post.updated_at == post.updated_at
    assert len(result_images) == len(image_urls)
    for image in result_images:
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

    post_service.post_repository.find_by_id.return_value = post
    post_service.post_image_repository.find_all_by_post_id.return_value = images

    # when
    found_post, found_images = post_service.get_post(post.id)

    # then
    assert found_post.id == post.id
    assert found_post.author_id == post.author_id
    assert found_post.title == post.title
    assert found_post.content == post.content
    assert len(found_images) == len(images)
    for found_image, image in zip(found_images, images):
        assert found_image.id == image.id
        assert found_image.post_id == image.post_id
        assert found_image.image_url == image.image_url


def test_update_post(post_service: PostService) -> None:
    # given
    post_id = str(ULID())
    author_id = str(ULID())
    original_post = Post(
        id=post_id,
        author_id=author_id,
        title="original title",
        content="original content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    updated_post = Post(
        id=post_id,
        author_id=author_id,
        title="updated title",
        content="updated content",
        created_at=original_post.created_at,
        updated_at=datetime.now(UTC),
    )

    updated_image_urls = [
        "https://example.com/updated_image1.png",
        "https://example.com/updated_image2.png",
    ]
    updated_images = [
        PostImage(
            id=str(ULID()),
            post_id=post_id,
            image_url=image_url,
        )
        for image_url in updated_image_urls
    ]

    post_service.post_repository.find_by_id.return_value = original_post
    post_service.post_repository.update.return_value = updated_post
    post_service.post_image_repository.delete_by_post_id.return_value = None
    post_service.post_image_repository.save.return_value = updated_images

    # when
    result_post, result_images = post_service.update_post(
        post_id=post_id,
        title="updated title",
        content="updated content",
        image_urls=updated_image_urls,
    )

    # then
    assert result_post.id == updated_post.id
    assert result_post.title == "updated title"
    assert result_post.content == "updated content"
    assert len(result_images) == len(updated_image_urls)
    for image in result_images:
        assert image.post_id == post_id
        assert image.image_url in updated_image_urls


def test_delete_post(post_service: PostService) -> None:
    # given
    post_id = str(ULID())
    post = Post(
        id=post_id,
        author_id=str(ULID()),
        title="title",
        content="content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    post_service.post_repository.find_by_id.return_value = post
    post_service.post_repository.delete.return_value = None
    post_service.post_image_repository.delete_by_post_id.return_value = None

    # when
    post_service.delete_post(post_id=post_id)

    # then
    # Verify that the post was found and delete methods were called
    post_service.post_repository.find_by_id.assert_called_once_with(post_id)
    post_service.post_repository.delete.assert_called_once_with(post_id)
    post_service.post_image_repository.delete_by_post_id.assert_called_once_with(
        post_id
    )
