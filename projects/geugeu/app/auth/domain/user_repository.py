from abc import ABC, abstractmethod

from app.auth.domain.user import User


class IUserRepository(ABC):
    @abstractmethod
    def find_by_email(self, email: str) -> User:
        raise NotImplementedError
