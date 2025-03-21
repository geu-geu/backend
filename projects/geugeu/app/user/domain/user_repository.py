from abc import ABC, abstractmethod

from app.user.domain.user import User


class IUserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: str) -> User | None:
        raise NotImplementedError
