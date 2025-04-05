from fastapi import Depends

from app.drawing.repositories.drawing_image_repository import IDrawingImageRepository
from app.drawing.repositories.drawing_image_repository_impl import (
    DrawingImageRepositoryImpl,
)
from app.drawing.repositories.drawing_repository import IDrawingRepository
from app.drawing.repositories.drawing_repository_impl import DrawingRepositoryImpl
from app.drawing.services.drawing_service import DrawingService


def drawing_repository() -> IDrawingRepository:
    return DrawingRepositoryImpl()


def drawing_image_repository() -> IDrawingImageRepository:
    return DrawingImageRepositoryImpl()


def drawing_service(
    drawing_repository: IDrawingRepository = Depends(drawing_repository),
    drawing_image_repository: IDrawingImageRepository = Depends(
        drawing_image_repository
    ),
) -> DrawingService:
    return DrawingService(
        drawing_repository=drawing_repository,
        drawing_image_repository=drawing_image_repository,
    )
