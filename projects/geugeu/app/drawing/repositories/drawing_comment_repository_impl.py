from typing import final, override

from sqlmodel import Session, select

from app.drawing.domain.drawing_comment import DrawingComment
from app.drawing.repositories.drawing_comment_repository import (
    IDrawingCommentRepository,
)
from app.models import DrawingComment as _DrawingComment


@final
class DrawingCommentRepositoryImpl(IDrawingCommentRepository):
    @override
    def save(self, session: Session, drawing_comment: DrawingComment) -> DrawingComment:
        _drawing_comment = _DrawingComment(
            id=drawing_comment.id,
            author_id=drawing_comment.author_id,
            drawing_id=drawing_comment.drawing_id,
            content=drawing_comment.content,
            created_at=drawing_comment.created_at,
            updated_at=drawing_comment.updated_at,
        )
        session.add(_drawing_comment)
        session.commit()
        session.refresh(_drawing_comment)
        return DrawingComment(
            id=_drawing_comment.id,
            author_id=_drawing_comment.author_id,
            drawing_id=_drawing_comment.drawing_id,
            content=_drawing_comment.content,
            created_at=_drawing_comment.created_at,
            updated_at=_drawing_comment.updated_at,
        )

    @override
    def find_all_by_drawing_id(
        self, session: Session, drawing_id: str
    ) -> list[DrawingComment]:
        _drawing_comments = session.exec(
            select(_DrawingComment).where(_DrawingComment.drawing_id == drawing_id)
        ).all()
        return [
            DrawingComment(
                id=_drawing_comment.id,
                author_id=_drawing_comment.author_id,
                drawing_id=_drawing_comment.drawing_id,
                content=_drawing_comment.content,
                created_at=_drawing_comment.created_at,
                updated_at=_drawing_comment.updated_at,
            )
            for _drawing_comment in _drawing_comments
        ]

    @override
    def delete_all_by_drawing_id(self, session: Session, drawing_id: str) -> None:
        _drawing_comments = session.exec(
            select(_DrawingComment).where(_DrawingComment.drawing_id == drawing_id)
        ).all()
        for _drawing_comment in _drawing_comments:
            session.delete(_drawing_comment)
        session.commit()

    @override
    def find_by_id(self, session: Session, comment_id: str) -> DrawingComment | None:
        _drawing_comment = session.get(_DrawingComment, comment_id)
        if _drawing_comment is None:
            return None
        return DrawingComment(
            id=_drawing_comment.id,
            author_id=_drawing_comment.author_id,
            drawing_id=_drawing_comment.drawing_id,
            content=_drawing_comment.content,
            created_at=_drawing_comment.created_at,
            updated_at=_drawing_comment.updated_at,
        )

    @override
    def update(
        self, session: Session, drawing_comment: DrawingComment
    ) -> DrawingComment:
        _drawing_comment = session.get(_DrawingComment, drawing_comment.id)
        if _drawing_comment is None:
            raise ValueError(f"Drawing comment with id {drawing_comment.id} not found")

        _drawing_comment.content = drawing_comment.content
        _drawing_comment.updated_at = drawing_comment.updated_at

        session.add(_drawing_comment)
        session.commit()
        session.refresh(_drawing_comment)

        return DrawingComment(
            id=_drawing_comment.id,
            author_id=_drawing_comment.author_id,
            drawing_id=_drawing_comment.drawing_id,
            content=_drawing_comment.content,
            created_at=_drawing_comment.created_at,
            updated_at=_drawing_comment.updated_at,
        )

    @override
    def delete(self, session: Session, comment_id: str) -> None:
        _drawing_comment = session.get(_DrawingComment, comment_id)
        if _drawing_comment is None:
            raise ValueError(f"Drawing comment with id {comment_id} not found")

        session.delete(_drawing_comment)
        session.commit()
