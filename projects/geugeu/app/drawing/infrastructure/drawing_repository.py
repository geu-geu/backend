from datetime import UTC, datetime
from typing import final, override

from sqlmodel import Session, select

from app.drawing.domain.drawing import Drawing, DrawingStatus
from app.drawing.domain.drawing_repository import IDrawingRepository
from app.models import Drawing as _Drawing


@final
class DrawingRepository(IDrawingRepository):
    @override
    def save(self, session: Session, drawing: Drawing) -> Drawing:
        _drawing = _Drawing(
            id=drawing.id,
            post_id=drawing.post_id,
            author_id=drawing.author_id,
            content=drawing.content,
            status=drawing.status,
            created_at=drawing.created_at,
            updated_at=drawing.updated_at,
        )
        session.add(_drawing)
        session.commit()
        session.refresh(_drawing)
        return Drawing(
            id=_drawing.id,
            post_id=_drawing.post_id,
            author_id=_drawing.author_id,
            content=_drawing.content,
            status=DrawingStatus(_drawing.status),
            created_at=_drawing.created_at,
            updated_at=_drawing.updated_at,
        )

    @override
    def find_by_id(self, session: Session, id: str) -> Drawing | None:
        _drawing = session.exec(select(_Drawing).where(_Drawing.id == id)).first()
        if not _drawing:
            return None
        return Drawing(
            id=_drawing.id,
            post_id=_drawing.post_id,
            author_id=_drawing.author_id,
            content=_drawing.content,
            status=DrawingStatus(_drawing.status),
            created_at=_drawing.created_at,
            updated_at=_drawing.updated_at,
        )

    @override
    def find_all_by_post_id(self, session: Session, post_id: str) -> list[Drawing]:
        _drawings = session.exec(
            select(_Drawing).where(_Drawing.post_id == post_id)
        ).all()
        return [
            Drawing(
                id=_drawing.id,
                post_id=_drawing.post_id,
                author_id=_drawing.author_id,
                content=_drawing.content,
                status=DrawingStatus(_drawing.status),
                created_at=_drawing.created_at,
                updated_at=_drawing.updated_at,
            )
            for _drawing in _drawings
        ]

    @override
    def update(self, session: Session, drawing: Drawing) -> Drawing:
        _drawing = session.exec(
            select(_Drawing).where(_Drawing.id == drawing.id)
        ).first()
        if not _drawing:
            raise ValueError(f"Drawing with id {drawing.id} not found")

        _drawing.post_id = drawing.post_id
        _drawing.author_id = drawing.author_id
        _drawing.content = drawing.content
        _drawing.status = drawing.status
        _drawing.updated_at = datetime.now(UTC)

        session.add(_drawing)
        session.commit()
        session.refresh(_drawing)

        return Drawing(
            id=_drawing.id,
            post_id=_drawing.post_id,
            author_id=_drawing.author_id,
            content=_drawing.content,
            status=DrawingStatus(_drawing.status),
            created_at=_drawing.created_at,
            updated_at=_drawing.updated_at,
        )

    @override
    def delete(self, session: Session, id: str) -> None:
        _drawing = session.exec(select(_Drawing).where(_Drawing.id == id)).first()
        if not _drawing:
            raise ValueError(f"Drawing with id {id} not found")
        session.delete(_drawing)
        session.commit()
