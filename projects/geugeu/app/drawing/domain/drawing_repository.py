from abc import ABC, abstractmethod

from app.drawing.domain.drawing import Drawing


class IDrawingRepository(ABC):
    @abstractmethod
    def save(self, drawing: Drawing) -> Drawing:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: str) -> Drawing | None:
        raise NotImplementedError

    @abstractmethod
    def find_all_by_post_id(self, post_id: str) -> list[Drawing]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str) -> None:
        raise NotImplementedError
