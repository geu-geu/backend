from datetime import UTC, datetime

import pytest
from fastapi import HTTPException
from sqlmodel import Session
from ulid import ULID

from app.post.domain.post import Post
from app.post.domain.post_comment import PostComment
from app.post.domain.post_image import PostImage
from app.post.repositories.post_comment_repository import IPostCommentRepository
from app.post.repositories.post_image_repository import IPostImageRepository
from app.post.repositories.post_repository import IPostRepository
from app.post.services.post_service import PostService


@pytest.fixture()
def post_service(
    post_repository: IPostRepository,
    post_image_repository: IPostImageRepository,
    post_comment_repository: IPostCommentRepository,
) -> PostService:
    return PostService(
        post_repository=post_repository,
        post_image_repository=post_image_repository,
        post_comment_repository=post_comment_repository,
    )


def test_create_post(post_service: PostService, session: Session) -> None:
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

    # when
    result_post, result_images = post_service.create_post(session, post, image_urls)

    # then
    assert result_post.id == post.id
    assert result_post.author_id == post.author_id
    assert result_post.title == post.title
    assert result_post.content == post.content
    assert len(result_images) == len(image_urls)
    for image in result_images:
        assert image.post_id == post.id
        assert image.image_url in image_urls


def test_get_post(
    post_service: PostService,
    post_repository: IPostRepository,
    post_image_repository: IPostImageRepository,
    session: Session,
) -> None:
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
    post_repository.save(session, post)
    post_image_repository.save(session, post.id, [image.image_url for image in images])

    # when
    found_post, found_images = post_service.get_post(session, post.id)

    # then
    assert found_post.id == post.id
    assert found_post.author_id == post.author_id
    assert found_post.title == post.title
    assert found_post.content == post.content
    assert len(found_images) == len(images)
    for found_image, image in zip(found_images, images):
        assert found_image.post_id == image.post_id
        assert found_image.image_url == image.image_url


def test_update_post(
    post_service: PostService, post_repository: IPostRepository, session: Session
) -> None:
    # given
    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title="original title",
        content="original content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_repository.save(session, post)

    new_title = "updated title"
    new_content = "updated content"
    new_image_urls = [
        "https://example.com/updated_image1.png",
        "https://example.com/updated_image2.png",
    ]

    # when
    result_post, result_images = post_service.update_post(
        session,
        post.id,
        new_title,
        new_content,
        new_image_urls,
    )

    # then
    assert result_post.id == post.id
    assert result_post.title == new_title
    assert result_post.content == new_content
    assert len(result_images) == len(new_image_urls)
    for image in result_images:
        assert image.post_id == post.id
        assert image.image_url in new_image_urls


def test_delete_post(
    post_service: PostService, post_repository: IPostRepository, session: Session
) -> None:
    # given
    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title="title",
        content="content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_repository.save(session, post)
    assert post_repository.find_by_id(session, post.id) is not None

    # when
    post_service.delete_post(session, post.id)

    # then
    assert post_repository.find_by_id(session, post.id) is None


def test_create_post_comment(
    post_service: PostService,
    post_repository: IPostRepository,
    session: Session,
) -> None:
    # given
    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title="title",
        content="content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_repository.save(session, post)

    post_comment = PostComment(
        id=str(ULID()),
        author_id=str(ULID()),
        post_id=post.id,
        content="comment",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    # when
    result = post_service.create_post_comment(session, post_comment)

    # then
    assert result.id == post_comment.id
    assert result.author_id == post_comment.author_id
    assert result.post_id == post_comment.post_id
    assert result.content == post_comment.content


def test_create_post_comment_with_nonexistent_post(
    post_service: PostService,
    session: Session,
) -> None:
    # given
    post_comment = PostComment(
        id=str(ULID()),
        author_id=str(ULID()),
        post_id=str(ULID()),  # nonexistent post id
        content="comment",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    # when & then
    with pytest.raises(HTTPException) as exc_info:
        post_service.create_post_comment(session, post_comment)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Post not found"


def test_get_post_comments(
    post_service: PostService,
    post_repository: IPostRepository,
    post_comment_repository: IPostCommentRepository,
    session: Session,
) -> None:
    # given
    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title="title",
        content="content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_repository.save(session, post)

    post_comment = PostComment(
        id=str(ULID()),
        author_id=str(ULID()),
        post_id=post.id,
        content="comment",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_comment_repository.save(session, post_comment)

    # when
    result = post_service.get_post_comments(session, post.id)

    # then
    assert len(result) == 1
    assert result[0].id == post_comment.id
    assert result[0].author_id == post_comment.author_id
    assert result[0].post_id == post_comment.post_id
    assert result[0].content == post_comment.content


def test_get_post_comments_with_nonexistent_post(
    post_service: PostService,
    session: Session,
) -> None:
    # when & then
    with pytest.raises(HTTPException) as exc_info:
        post_service.get_post_comments(session, str(ULID()))
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Post not found"


def test_update_post_comment(
    post_service: PostService,
    post_repository: IPostRepository,
    post_comment_repository: IPostCommentRepository,
    session: Session,
) -> None:
    # given
    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title="title",
        content="content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_repository.save(session, post)

    author_id = str(ULID())
    post_comment = PostComment(
        id=str(ULID()),
        author_id=author_id,
        post_id=post.id,
        content="original comment",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_comment_repository.save(session, post_comment)

    new_content = "updated comment"

    # when
    result = post_service.update_post_comment(
        session, post.id, post_comment.id, new_content, author_id
    )

    # then
    assert result.id == post_comment.id
    assert result.author_id == post_comment.author_id
    assert result.post_id == post_comment.post_id
    assert result.content == new_content


def test_update_post_comment_with_nonexistent_post(
    post_service: PostService,
    session: Session,
) -> None:
    # when & then
    with pytest.raises(HTTPException) as exc_info:
        post_service.update_post_comment(
            session, str(ULID()), str(ULID()), "content", str(ULID())
        )
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Post not found"


def test_update_post_comment_with_nonexistent_comment(
    post_service: PostService,
    post_repository: IPostRepository,
    session: Session,
) -> None:
    # given
    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title="title",
        content="content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_repository.save(session, post)

    # when & then
    with pytest.raises(HTTPException) as exc_info:
        post_service.update_post_comment(
            session, post.id, str(ULID()), "content", str(ULID())
        )
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Post comment not found"


def test_update_post_comment_with_unauthorized_user(
    post_service: PostService,
    post_repository: IPostRepository,
    post_comment_repository: IPostCommentRepository,
    session: Session,
) -> None:
    # given
    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title="title",
        content="content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_repository.save(session, post)

    post_comment = PostComment(
        id=str(ULID()),
        author_id=str(ULID()),
        post_id=post.id,
        content="comment",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_comment_repository.save(session, post_comment)

    # when & then
    with pytest.raises(HTTPException) as exc_info:
        post_service.update_post_comment(
            session, post.id, post_comment.id, "content", str(ULID())
        )
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You are not the author of this comment"


def test_delete_post_comment(
    post_service: PostService,
    post_repository: IPostRepository,
    post_comment_repository: IPostCommentRepository,
    session: Session,
) -> None:
    # given
    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title="title",
        content="content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_repository.save(session, post)

    author_id = str(ULID())
    post_comment = PostComment(
        id=str(ULID()),
        author_id=author_id,
        post_id=post.id,
        content="comment",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_comment_repository.save(session, post_comment)
    assert post_comment_repository.find_by_id(session, post_comment.id) is not None

    # when
    post_service.delete_post_comment(session, post.id, post_comment.id, author_id)

    # then
    assert post_comment_repository.find_by_id(session, post_comment.id) is None


def test_delete_post_comment_with_nonexistent_post(
    post_service: PostService,
    session: Session,
) -> None:
    # when & then
    with pytest.raises(HTTPException) as exc_info:
        post_service.delete_post_comment(
            session, str(ULID()), str(ULID()), str(ULID())
        )
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Post not found"


def test_delete_post_comment_with_nonexistent_comment(
    post_service: PostService,
    post_repository: IPostRepository,
    session: Session,
) -> None:
    # given
    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title="title",
        content="content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_repository.save(session, post)

    # when & then
    with pytest.raises(HTTPException) as exc_info:
        post_service.delete_post_comment(
            session, post.id, str(ULID()), str(ULID())
        )
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Post comment not found"


def test_delete_post_comment_with_unauthorized_user(
    post_service: PostService,
    post_repository: IPostRepository,
    post_comment_repository: IPostCommentRepository,
    session: Session,
) -> None:
    # given
    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title="title",
        content="content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_repository.save(session, post)

    post_comment = PostComment(
        id=str(ULID()),
        author_id=str(ULID()),
        post_id=post.id,
        content="comment",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_comment_repository.save(session, post_comment)

    # when & then
    with pytest.raises(HTTPException) as exc_info:
        post_service.delete_post_comment(
            session, post.id, post_comment.id, str(ULID())
        )
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You are not the author of this comment"
