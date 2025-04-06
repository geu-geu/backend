from fastapi import Depends

from app.drawing.repositories.drawing_comment_repository import (
    IDrawingCommentRepository,
)
from app.drawing.repositories.drawing_comment_repository_impl import (
    DrawingCommentRepositoryImpl,
)
from app.drawing.repositories.drawing_image_repository import IDrawingImageRepository
from app.drawing.repositories.drawing_image_repository_impl import (
    DrawingImageRepositoryImpl,
)
from app.drawing.repositories.drawing_repository import IDrawingRepository
from app.drawing.repositories.drawing_repository_impl import DrawingRepositoryImpl
from app.drawing.repositories.post_repository import IPostRepository
from app.drawing.repositories.post_repository_impl import PostRepositoryImpl
from app.drawing.services.drawing_service import DrawingService


def drawing_repository() -> IDrawingRepository:
    return DrawingRepositoryImpl()


def drawing_image_repository() -> IDrawingImageRepository:
    return DrawingImageRepositoryImpl()


def drawing_comment_repository() -> IDrawingCommentRepository:
    return DrawingCommentRepositoryImpl()


def post_repository() -> IPostRepository:
    return PostRepositoryImpl()


def drawing_service(
    drawing_repository: IDrawingRepository = Depends(drawing_repository),
    drawing_image_repository: IDrawingImageRepository = Depends(
        drawing_image_repository
    ),
    drawing_comment_repository: IDrawingCommentRepository = Depends(
        drawing_comment_repository
    ),
    post_repository: IPostRepository = Depends(post_repository),
) -> DrawingService:
    return DrawingService(
        drawing_repository=drawing_repository,
        drawing_image_repository=drawing_image_repository,
        drawing_comment_repository=drawing_comment_repository,
        post_repository=post_repository,
    )
