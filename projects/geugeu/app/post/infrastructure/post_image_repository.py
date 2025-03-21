from typing import final, override

from sqlmodel import Session
from ulid import ULID

from app.database import engine
from app.models import PostImage as _PostImage
from app.post.domain.post_image import PostImage
from app.post.domain.post_image_repository import IPostImageRepository


@final
class PostImageRepository(IPostImageRepository):
    @override
    def save(self, post_id: str, image_urls: list[str]) -> list[PostImage]:
        if not image_urls:
            return []
        _post_images = [
            _PostImage(
                id=str(ULID()),
                post_id=post_id,
                image_url=image_url,
            )
            for image_url in image_urls
        ]
        with Session(engine) as session:
            session.add_all(_post_images)
            session.commit()
            for _post_image in _post_images:
                session.refresh(_post_image)
        return [
            PostImage(
                id=_post_image.id,
                post_id=_post_image.post_id,
                image_url=_post_image.image_url,
            )
            for _post_image in _post_images
        ]
