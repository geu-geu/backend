from abc import ABC, abstractmethod

from sqlmodel import Session

from app.auth.domain.user import User


class IUserRepository(ABC):
    @abstractmethod
    def find_by_email(self, session: Session, email: str) -> User | None:
        raise NotImplementedError
