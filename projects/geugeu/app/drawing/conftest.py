import pytest

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


@pytest.fixture()
def drawing_repository() -> IDrawingRepository:
    return DrawingRepositoryImpl()


@pytest.fixture()
def drawing_image_repository() -> IDrawingImageRepository:
    return DrawingImageRepositoryImpl()


@pytest.fixture()
def drawing_comment_repository() -> IDrawingCommentRepository:
    return DrawingCommentRepositoryImpl()


@pytest.fixture()
def post_repository() -> IPostRepository:
    return PostRepositoryImpl()


@pytest.fixture()
def drawing_service(
    drawing_repository: IDrawingRepository,
    drawing_image_repository: IDrawingImageRepository,
    drawing_comment_repository: IDrawingCommentRepository,
    post_repository: IPostRepository,
) -> DrawingService:
    return DrawingService(
        drawing_repository=drawing_repository,
        drawing_image_repository=drawing_image_repository,
        drawing_comment_repository=drawing_comment_repository,
        post_repository=post_repository,
    )
