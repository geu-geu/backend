from abc import ABC, abstractmethod

from app.drawing.domain.drawing_image import DrawingImage


class IDrawingImageRepository(ABC):
    @abstractmethod
    def save(self, drawing_id: str, image_urls: list[str]) -> list[DrawingImage]:
        raise NotImplementedError

    @abstractmethod
    def find_all_by_drawing_id(self, drawing_id: str) -> list[DrawingImage]:
        raise NotImplementedError

    @abstractmethod
    def delete_by_drawing_id(self, drawing_id: str) -> None:
        raise NotImplementedError
