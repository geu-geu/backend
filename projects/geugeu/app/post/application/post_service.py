from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlmodel import Session

from app.post.domain.post import Post
from app.post.domain.post_comment import PostComment
from app.post.domain.post_comment_repository import IPostCommentRepository
from app.post.domain.post_image import PostImage
from app.post.domain.post_image_repository import IPostImageRepository
from app.post.domain.post_repository import IPostRepository


class PostService:
    def __init__(
        self,
        post_repository: IPostRepository,
        post_image_repository: IPostImageRepository,
        post_comment_repository: IPostCommentRepository,
    ):
        self.post_repository = post_repository
        self.post_image_repository = post_image_repository
        self.post_comment_repository = post_comment_repository

    def create_post(
        self, session: Session, post: Post, image_urls: list[str]
    ) -> tuple[Post, list[PostImage]]:
        post = self.post_repository.save(session, post)
        images = self.post_image_repository.save(session, post.id, image_urls)
        return post, images

    def get_post(self, session: Session, post_id: str) -> tuple[Post, list[PostImage]]:
        post = self.post_repository.find_by_id(session, post_id)
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found",
            )
        images = self.post_image_repository.find_all_by_post_id(session, post_id)
        return post, images

    def update_post(
        self,
        session: Session,
        post_id: str,
        title: str,
        content: str,
        image_urls: list[str],
    ) -> tuple[Post, list[PostImage]]:
        post = self.post_repository.find_by_id(session, post_id)
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found",
            )

        updated_post = Post(
            id=post.id,
            author_id=post.author_id,
            title=title,
            content=content,
            created_at=post.created_at,
            updated_at=datetime.now(UTC),
        )

        self.post_image_repository.delete_by_post_id(session, post_id)
        updated_post = self.post_repository.update(session, updated_post)
        images = self.post_image_repository.save(session, post_id, image_urls)

        return updated_post, images

    def delete_post(self, session: Session, post_id: str) -> None:
        post = self.post_repository.find_by_id(session, post_id)
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found",
            )

        self.post_image_repository.delete_by_post_id(session, post_id)
        self.post_repository.delete(session, post_id)

    def create_post_comment(
        self, session: Session, post_comment: PostComment
    ) -> PostComment:
        post_comment = self.post_comment_repository.save(session, post_comment)
        return post_comment

    def get_post_comments(self, session: Session, post_id: str) -> list[PostComment]:
        return self.post_comment_repository.find_all_by_post_id(session, post_id)
