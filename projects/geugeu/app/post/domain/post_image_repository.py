from abc import ABC, abstractmethod

from app.post.domain.post_image import PostImage


class IPostImageRepository(ABC):
    @abstractmethod
    def save(self, post_id: str, image_urls: list[str]) -> list[PostImage]:
        raise NotImplementedError

    @abstractmethod
    def find_all_by_post_id(self, post_id: str) -> list[PostImage]:
        raise NotImplementedError

    @abstractmethod
    def delete_by_post_id(self, post_id: str) -> None:
        raise NotImplementedError
