from typing import final, override

from sqlmodel import Session, select
from ulid import ULID

from app.database import engine
from app.drawing.domain.drawing_image import DrawingImage
from app.drawing.domain.drawing_image_repository import IDrawingImageRepository
from app.models import DrawingImage as _DrawingImage


@final
class DrawingImageRepository(IDrawingImageRepository):
    @override
    def save(self, drawing_id: str, image_urls: list[str]) -> list[DrawingImage]:
        if not image_urls:
            return []
        _drawing_images = [
            _DrawingImage(
                id=str(ULID()),
                drawing_id=drawing_id,
                image_url=image_url,
            )
            for image_url in image_urls
        ]
        with Session(engine) as session:
            session.add_all(_drawing_images)
            session.commit()
            for _drawing_image in _drawing_images:
                session.refresh(_drawing_image)
        return [
            DrawingImage(
                id=_drawing_image.id,
                drawing_id=_drawing_image.drawing_id,
                image_url=_drawing_image.image_url,
            )
            for _drawing_image in _drawing_images
        ]

    @override
    def find_all_by_drawing_id(self, drawing_id: str) -> list[DrawingImage]:
        with Session(engine) as session:
            _drawing_images = session.exec(
                select(_DrawingImage).where(_DrawingImage.drawing_id == drawing_id)
            ).all()
        return [
            DrawingImage(
                id=_drawing_image.id,
                drawing_id=_drawing_image.drawing_id,
                image_url=_drawing_image.image_url,
            )
            for _drawing_image in _drawing_images
        ]

    @override
    def delete_by_drawing_id(self, drawing_id: str) -> None:
        with Session(engine) as session:
            _drawing_images = session.exec(
                select(_DrawingImage).where(_DrawingImage.drawing_id == drawing_id)
            ).all()
            for _drawing_image in _drawing_images:
                session.delete(_drawing_image)
            session.commit()
