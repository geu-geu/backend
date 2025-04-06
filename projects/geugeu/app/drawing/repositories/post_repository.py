from abc import ABC, abstractmethod

from sqlmodel import Session

from app.drawing.domain.post import Post


class IPostRepository(ABC):
    @abstractmethod
    def find_by_id(self, session: Session, id: str) -> Post | None:
        pass
