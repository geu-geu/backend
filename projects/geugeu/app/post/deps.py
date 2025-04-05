from fastapi import Depends

from app.post.repositories.post_comment_repository import IPostCommentRepository
from app.post.repositories.post_comment_repository_impl import PostCommentRepositoryImpl
from app.post.repositories.post_image_repository import IPostImageRepository
from app.post.repositories.post_image_repository_impl import PostImageRepositoryImpl
from app.post.repositories.post_repository import IPostRepository
from app.post.repositories.post_repository_impl import PostRepositoryImpl
from app.post.services.post_service import PostService


def post_repository() -> IPostRepository:
    return PostRepositoryImpl()


def post_image_repository() -> IPostImageRepository:
    return PostImageRepositoryImpl()


def post_comment_repository() -> IPostCommentRepository:
    return PostCommentRepositoryImpl()


def post_service(
    post_repository: IPostRepository = Depends(post_repository),
    post_image_repository: IPostImageRepository = Depends(post_image_repository),
    post_comment_repository: IPostCommentRepository = Depends(post_comment_repository),
) -> PostService:
    return PostService(post_repository, post_image_repository, post_comment_repository)
