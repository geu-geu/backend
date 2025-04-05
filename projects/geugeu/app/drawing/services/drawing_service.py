from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlmodel import Session

from app.drawing.domain.drawing import Drawing, DrawingStatus
from app.drawing.domain.drawing_comment import DrawingComment
from app.drawing.domain.drawing_image import DrawingImage
from app.drawing.repositories.drawing_comment_repository import (
    IDrawingCommentRepository,
)
from app.drawing.repositories.drawing_image_repository import IDrawingImageRepository
from app.drawing.repositories.drawing_repository import IDrawingRepository


class DrawingService:
    def __init__(
        self,
        drawing_repository: IDrawingRepository,
        drawing_image_repository: IDrawingImageRepository,
        drawing_comment_repository: IDrawingCommentRepository,
    ):
        self.drawing_repository = drawing_repository
        self.drawing_image_repository = drawing_image_repository
        self.drawing_comment_repository = drawing_comment_repository

    def create_drawing(
        self, session: Session, drawing: Drawing, image_urls: list[str]
    ) -> tuple[Drawing, list[DrawingImage]]:
        drawing = self.drawing_repository.save(session, drawing)
        images = self.drawing_image_repository.save(session, drawing.id, image_urls)
        return drawing, images

    def get_drawing(
        self, session: Session, drawing_id: str
    ) -> tuple[Drawing, list[DrawingImage]]:
        drawing = self.drawing_repository.find_by_id(session, drawing_id)
        if drawing is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Drawing not found",
            )
        images = self.drawing_image_repository.find_all_by_drawing_id(
            session, drawing_id
        )
        return drawing, images

    def get_drawings_by_post_id(
        self, session: Session, post_id: str
    ) -> list[tuple[Drawing, list[DrawingImage]]]:
        drawings = self.drawing_repository.find_all_by_post_id(session, post_id)
        return [
            (
                drawing,
                self.drawing_image_repository.find_all_by_drawing_id(
                    session, drawing.id
                ),
            )
            for drawing in drawings
        ]

    def delete_drawing(self, session: Session, drawing_id: str) -> None:
        drawing = self.drawing_repository.find_by_id(session, drawing_id)
        if drawing is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Drawing not found",
            )
        self.drawing_image_repository.delete_by_drawing_id(session, drawing_id)
        self.drawing_repository.delete(session, drawing_id)

    def complete_drawing(
        self, session: Session, drawing_id: str, content: str, image_urls: list[str]
    ) -> tuple[Drawing, list[DrawingImage]]:
        drawing = self.drawing_repository.find_by_id(session, drawing_id)
        if drawing is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Drawing not found",
            )

        if drawing.status == DrawingStatus.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Drawing is already completed",
            )

        drawing.content = content
        drawing.status = DrawingStatus.COMPLETED
        drawing.updated_at = datetime.now(UTC)
        updated_drawing = self.drawing_repository.update(session, drawing)

        # Delete existing images and save new ones
        self.drawing_image_repository.delete_by_drawing_id(session, drawing_id)
        images = self.drawing_image_repository.save(session, drawing_id, image_urls)

        return updated_drawing, images

    def update_drawing(
        self, session: Session, drawing_id: str, content: str, image_urls: list[str]
    ) -> tuple[Drawing, list[DrawingImage]]:
        drawing = self.drawing_repository.find_by_id(session, drawing_id)
        if drawing is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Drawing not found",
            )

        drawing.content = content
        updated_drawing = self.drawing_repository.update(session, drawing)

        # Delete existing images and save new ones
        self.drawing_image_repository.delete_by_drawing_id(session, drawing_id)
        images = self.drawing_image_repository.save(session, drawing_id, image_urls)

        return updated_drawing, images

    def create_drawing_comment(
        self, session: Session, drawing_comment: DrawingComment
    ) -> DrawingComment:
        # Check if drawing exists
        drawing = self.drawing_repository.find_by_id(
            session, drawing_comment.drawing_id
        )
        if drawing is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Drawing not found",
            )

        drawing_comment = self.drawing_comment_repository.save(session, drawing_comment)
        return drawing_comment

    def get_drawing_comments(
        self, session: Session, drawing_id: str
    ) -> list[DrawingComment]:
        # Check if drawing exists
        drawing = self.drawing_repository.find_by_id(session, drawing_id)
        if drawing is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Drawing not found",
            )

        return self.drawing_comment_repository.find_all_by_drawing_id(
            session, drawing_id
        )

    def update_drawing_comment(
        self,
        session: Session,
        drawing_id: str,
        comment_id: str,
        content: str,
        author_id: str,
    ) -> DrawingComment:
        # Check if drawing exists
        drawing = self.drawing_repository.find_by_id(session, drawing_id)
        if drawing is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Drawing not found",
            )

        drawing_comment = self.drawing_comment_repository.find_by_id(
            session, comment_id
        )
        if drawing_comment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Drawing comment not found",
            )

        # Check if the user is the author of the comment
        if drawing_comment.author_id != author_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not the author of this comment",
            )

        drawing_comment.content = content
        drawing_comment.updated_at = datetime.now(UTC)
        drawing_comment = self.drawing_comment_repository.update(
            session, drawing_comment
        )
        return drawing_comment

    def delete_drawing_comment(
        self, session: Session, drawing_id: str, comment_id: str, author_id: str
    ) -> None:
        # Check if drawing exists
        drawing = self.drawing_repository.find_by_id(session, drawing_id)
        if drawing is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Drawing not found",
            )

        drawing_comment = self.drawing_comment_repository.find_by_id(
            session, comment_id
        )
        if drawing_comment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Drawing comment not found",
            )

        # Check if the user is the author of the comment
        if drawing_comment.author_id != author_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not the author of this comment",
            )

        self.drawing_comment_repository.delete(session, comment_id)
