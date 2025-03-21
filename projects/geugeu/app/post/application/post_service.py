from fastapi import HTTPException, status

from app.post.domain.post import Post
from app.post.domain.post_image import PostImage
from app.post.domain.post_image_repository import IPostImageRepository
from app.post.domain.post_repository import IPostRepository


class PostService:
    def __init__(
        self,
        post_repository: IPostRepository,
        post_image_repository: IPostImageRepository,
    ):
        self.post_repository = post_repository
        self.post_image_repository = post_image_repository

    def create_post(
        self, post: Post, image_urls: list[str]
    ) -> tuple[Post, list[PostImage]]:
        post = self.post_repository.save(post)
        images = self.post_image_repository.save(post.id, image_urls)
        return post, images

    def get_post(self, post_id: str) -> Post:
        post = self.post_repository.find_by_id(post_id)
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found",
            )
        return post
