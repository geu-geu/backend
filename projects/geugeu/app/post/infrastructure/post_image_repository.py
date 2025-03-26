from typing import final, override

from sqlmodel import Session, select
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

    @override
    def find_all_by_post_id(self, post_id: str) -> list[PostImage]:
        with Session(engine) as session:
            _post_images = session.exec(
                select(_PostImage).where(_PostImage.post_id == post_id)
            ).all()
        return [
            PostImage(
                id=_post_image.id,
                post_id=_post_image.post_id,
                image_url=_post_image.image_url,
            )
            for _post_image in _post_images
        ]

    @override
    def delete_by_post_id(self, post_id: str) -> None:
        with Session(engine) as session:
            _post_images = session.exec(
                select(_PostImage).where(_PostImage.post_id == post_id)
            ).all()
            for _post_image in _post_images:
                session.delete(_post_image)
            session.commit()
