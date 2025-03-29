from abc import ABC, abstractmethod

from sqlmodel import Session

from app.drawing.domain.drawing import Drawing


class IDrawingRepository(ABC):
    @abstractmethod
    def save(self, session: Session, drawing: Drawing) -> Drawing:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, session: Session, id: str) -> Drawing | None:
        raise NotImplementedError

    @abstractmethod
    def find_all_by_post_id(self, session: Session, post_id: str) -> list[Drawing]:
        raise NotImplementedError

    @abstractmethod
    def update(self, session: Session, drawing: Drawing) -> Drawing:
        raise NotImplementedError

    @abstractmethod
    def delete(self, session: Session, id: str) -> None:
        raise NotImplementedError
