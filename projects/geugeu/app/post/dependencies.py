from fastapi import Depends

from app.post.application.post_service import PostService
from app.post.domain.post_comment_repository import IPostCommentRepository
from app.post.domain.post_image_repository import IPostImageRepository
from app.post.domain.post_repository import IPostRepository
from app.post.infrastructure.post_comment_repository import PostCommentRepository
from app.post.infrastructure.post_image_repository import PostImageRepository
from app.post.infrastructure.post_repository import PostRepository


def post_repository() -> IPostRepository:
    return PostRepository()


def post_image_repository() -> IPostImageRepository:
    return PostImageRepository()


def post_comment_repository() -> IPostCommentRepository:
    return PostCommentRepository()


def post_service(
    post_repository: IPostRepository = Depends(post_repository),
    post_image_repository: IPostImageRepository = Depends(post_image_repository),
    post_comment_repository: IPostCommentRepository = Depends(post_comment_repository),
) -> PostService:
    return PostService(post_repository, post_image_repository, post_comment_repository)
