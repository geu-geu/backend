import pytest

from app.drawing.repositories.drawing_image_repository import IDrawingImageRepository
from app.drawing.repositories.drawing_image_repository_impl import (
    DrawingImageRepositoryImpl,
)
from app.drawing.repositories.drawing_repository import IDrawingRepository
from app.drawing.repositories.drawing_repository_impl import DrawingRepositoryImpl
from app.drawing.services.drawing_service import DrawingService


@pytest.fixture()
def drawing_repository() -> IDrawingRepository:
    return DrawingRepositoryImpl()


@pytest.fixture()
def drawing_image_repository() -> IDrawingImageRepository:
    return DrawingImageRepositoryImpl()


@pytest.fixture()
def drawing_service(
    drawing_repository: IDrawingRepository,
    drawing_image_repository: IDrawingImageRepository,
) -> DrawingService:
    return DrawingService(
        drawing_repository=drawing_repository,
        drawing_image_repository=drawing_image_repository,
    )
