from abc import ABC, abstractmethod

from sqlmodel import Session

from app.post.domain.post import Post


class IPostRepository(ABC):
    @abstractmethod
    def save(self, session: Session, post: Post) -> Post:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, session: Session, id: str) -> Post | None:
        raise NotImplementedError

    @abstractmethod
    def update(self, session: Session, post: Post) -> Post:
        raise NotImplementedError

    @abstractmethod
    def delete(self, session: Session, id: str) -> None:
        raise NotImplementedError
