import pytest

from app.drawing.application.drawing_service import DrawingService
from app.drawing.domain.drawing_image_repository import IDrawingImageRepository
from app.drawing.domain.drawing_repository import IDrawingRepository
from app.drawing.infrastructure.drawing_image_repository import DrawingImageRepository
from app.drawing.infrastructure.drawing_repository import DrawingRepository


@pytest.fixture()
def drawing_repository() -> IDrawingRepository:
    return DrawingRepository()


@pytest.fixture()
def drawing_image_repository() -> IDrawingImageRepository:
    return DrawingImageRepository()


@pytest.fixture()
def drawing_service(
    drawing_repository: IDrawingRepository,
    drawing_image_repository: IDrawingImageRepository,
) -> DrawingService:
    return DrawingService(
        drawing_repository=drawing_repository,
        drawing_image_repository=drawing_image_repository,
    )
