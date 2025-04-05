from abc import ABC, abstractmethod

from sqlmodel import Session

from app.drawing.domain.drawing_comment import DrawingComment


class IDrawingCommentRepository(ABC):
    @abstractmethod
    def save(self, session: Session, drawing_comment: DrawingComment) -> DrawingComment:
        raise NotImplementedError

    @abstractmethod
    def find_all_by_drawing_id(
        self, session: Session, drawing_id: str
    ) -> list[DrawingComment]:
        raise NotImplementedError

    @abstractmethod
    def delete_all_by_drawing_id(self, session: Session, drawing_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, session: Session, comment_id: str) -> DrawingComment | None:
        raise NotImplementedError

    @abstractmethod
    def update(
        self, session: Session, drawing_comment: DrawingComment
    ) -> DrawingComment:
        raise NotImplementedError

    @abstractmethod
    def delete(self, session: Session, comment_id: str) -> None:
        raise NotImplementedError
