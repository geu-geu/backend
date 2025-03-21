from abc import ABC, abstractmethod

from app.post.domain.post import Post


class IPostRepository(ABC):
    @abstractmethod
    def save(self, post: Post) -> Post:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: str) -> Post | None:
        raise NotImplementedError
