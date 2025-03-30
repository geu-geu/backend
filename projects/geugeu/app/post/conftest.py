import pytest

from app.post.domain.post_comment_repository import IPostCommentRepository
from app.post.domain.post_image_repository import IPostImageRepository
from app.post.domain.post_repository import IPostRepository
from app.post.infrastructure.post_comment_repository import PostCommentRepository
from app.post.infrastructure.post_image_repository import PostImageRepository
from app.post.infrastructure.post_repository import PostRepository


@pytest.fixture()
def post_repository() -> IPostRepository:
    return PostRepository()


@pytest.fixture()
def post_image_repository() -> IPostImageRepository:
    return PostImageRepository()


@pytest.fixture()
def post_comment_repository() -> IPostCommentRepository:
    return PostCommentRepository()
