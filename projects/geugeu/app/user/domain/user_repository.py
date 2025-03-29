from abc import ABC, abstractmethod

from sqlmodel import Session

from app.user.domain.user import User


class IUserRepository(ABC):
    @abstractmethod
    def save(self, session: Session, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, session: Session, id: str) -> User | None:
        raise NotImplementedError
