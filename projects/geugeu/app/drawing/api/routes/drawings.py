from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status
from ulid import ULID

from app.auth.deps import CurrentUserDep
from app.database import SessionDep
from app.drawing.api.schemas.drawings import (
    CompleteDrawingBody,
    CreateDrawingBody,
    CreateDrawingCommentBody,
    DrawingCommentResponse,
    DrawingResponse,
    UpdateDrawingBody,
    UpdateDrawingCommentBody,
)
from app.drawing.deps import drawing_service
from app.drawing.domain.drawing import Drawing, DrawingStatus
from app.drawing.domain.drawing_comment import DrawingComment
from app.drawing.services.drawing_service import DrawingService

router = APIRouter(prefix="/drawings", tags=["drawings"])


@router.get("/by-post/{post_id}", response_model=list[DrawingResponse])
async def get_drawings_by_post_id(
    post_id: str,
    drawing_service: Annotated[DrawingService, Depends(drawing_service)],
    session: SessionDep,
    user: CurrentUserDep,
) -> list[DrawingResponse]:
    drawings_with_images = drawing_service.get_drawings_by_post_id(
        session, post_id=post_id
    )
    return [
        DrawingResponse(
            id=drawing.id,
            post_id=drawing.post_id,
            content=drawing.content,
            images=[image.image_url for image in images],
            status=drawing.status,
            created_at=drawing.created_at,
            updated_at=drawing.updated_at,
        )
        for drawing, images in drawings_with_images
    ]


@router.post("/", response_model=DrawingResponse, status_code=status.HTTP_201_CREATED)
async def create_drawing(
    body: CreateDrawingBody,
    drawing_service: Annotated[DrawingService, Depends(drawing_service)],
    session: SessionDep,
    user: CurrentUserDep,
) -> DrawingResponse:
    drawing = Drawing(
        id=str(ULID()),
        post_id=body.post_id,
        author_id=user.id,
        content=body.content,
        status=DrawingStatus.DRAFT,  # 초기 상태는 DRAFT
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing, images = drawing_service.create_drawing(
        session,
        drawing=drawing,
        image_urls=[str(url) for url in body.image_urls],
    )
    return DrawingResponse(
        id=drawing.id,
        post_id=drawing.post_id,
        content=drawing.content,
        images=[image.image_url for image in images],
        status=drawing.status,
        created_at=drawing.created_at,
        updated_at=drawing.updated_at,
    )


@router.get("/{drawing_id}", response_model=DrawingResponse)
async def get_drawing(
    drawing_id: str,
    drawing_service: Annotated[DrawingService, Depends(drawing_service)],
    session: SessionDep,
    user: CurrentUserDep,
) -> DrawingResponse:
    drawing, images = drawing_service.get_drawing(session, drawing_id=drawing_id)
    return DrawingResponse(
        id=drawing.id,
        post_id=drawing.post_id,
        content=drawing.content,
        images=[image.image_url for image in images],
        status=drawing.status,
        created_at=drawing.created_at,
        updated_at=drawing.updated_at,
    )


@router.put("/{drawing_id}", response_model=DrawingResponse)
async def update_drawing(
    drawing_id: str,
    body: UpdateDrawingBody,
    drawing_service: Annotated[DrawingService, Depends(drawing_service)],
    session: SessionDep,
    user: CurrentUserDep,
) -> DrawingResponse:
    drawing, images = drawing_service.update_drawing(
        session,
        drawing_id=drawing_id,
        content=body.content,
        image_urls=body.image_urls,
    )
    return DrawingResponse(
        id=drawing.id,
        post_id=drawing.post_id,
        content=drawing.content,
        images=[image.image_url for image in images],
        status=drawing.status,
        created_at=drawing.created_at,
        updated_at=drawing.updated_at,
    )


@router.post("/{drawing_id}/complete", response_model=DrawingResponse)
async def complete_drawing(
    drawing_id: str,
    body: CompleteDrawingBody,
    drawing_service: Annotated[DrawingService, Depends(drawing_service)],
    session: SessionDep,
    user: CurrentUserDep,
) -> DrawingResponse:
    drawing, images = drawing_service.complete_drawing(
        session,
        drawing_id=drawing_id,
        content=body.content,
        image_urls=body.image_urls,
    )
    return DrawingResponse(
        id=drawing.id,
        post_id=drawing.post_id,
        content=drawing.content,
        images=[image.image_url for image in images],
        status=drawing.status,
        created_at=drawing.created_at,
        updated_at=drawing.updated_at,
    )


@router.delete("/{drawing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_drawing(
    drawing_id: str,
    drawing_service: Annotated[DrawingService, Depends(drawing_service)],
    session: SessionDep,
    user: CurrentUserDep,
) -> None:
    drawing_service.delete_drawing(session, drawing_id=drawing_id)


@router.post(
    "/{drawing_id}/comments",
    response_model=DrawingCommentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_drawing_comment(
    drawing_id: str,
    body: CreateDrawingCommentBody,
    drawing_service: Annotated[DrawingService, Depends(drawing_service)],
    session: SessionDep,
    user: CurrentUserDep,
) -> DrawingCommentResponse:
    drawing_comment = DrawingComment(
        id=str(ULID()),
        author_id=user.id,
        drawing_id=drawing_id,
        content=body.content,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing_comment = drawing_service.create_drawing_comment(
        session, drawing_comment=drawing_comment
    )
    return DrawingCommentResponse(
        id=drawing_comment.id,
        author_id=drawing_comment.author_id,
        drawing_id=drawing_comment.drawing_id,
        content=drawing_comment.content,
        created_at=drawing_comment.created_at,
        updated_at=drawing_comment.updated_at,
    )


@router.get("/{drawing_id}/comments", response_model=list[DrawingCommentResponse])
async def get_drawing_comments(
    drawing_id: str,
    drawing_service: Annotated[DrawingService, Depends(drawing_service)],
    session: SessionDep,
    user: CurrentUserDep,
) -> list[DrawingCommentResponse]:
    drawing_comments = drawing_service.get_drawing_comments(
        session, drawing_id=drawing_id
    )
    return [
        DrawingCommentResponse(
            id=drawing_comment.id,
            author_id=drawing_comment.author_id,
            drawing_id=drawing_comment.drawing_id,
            content=drawing_comment.content,
            created_at=drawing_comment.created_at,
            updated_at=drawing_comment.updated_at,
        )
        for drawing_comment in drawing_comments
    ]


@router.put(
    "/{drawing_id}/comments/{comment_id}", response_model=DrawingCommentResponse
)
async def update_drawing_comment(
    drawing_id: str,
    comment_id: str,
    body: UpdateDrawingCommentBody,
    drawing_service: Annotated[DrawingService, Depends(drawing_service)],
    session: SessionDep,
    user: CurrentUserDep,
) -> DrawingCommentResponse:
    drawing_comment = drawing_service.update_drawing_comment(
        session,
        drawing_id=drawing_id,
        comment_id=comment_id,
        content=body.content,
        author_id=user.id,
    )
    return DrawingCommentResponse(
        id=drawing_comment.id,
        author_id=drawing_comment.author_id,
        drawing_id=drawing_comment.drawing_id,
        content=drawing_comment.content,
        created_at=drawing_comment.created_at,
        updated_at=drawing_comment.updated_at,
    )


@router.delete(
    "/{drawing_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_drawing_comment(
    drawing_id: str,
    comment_id: str,
    drawing_service: Annotated[DrawingService, Depends(drawing_service)],
    session: SessionDep,
    user: CurrentUserDep,
) -> None:
    drawing_service.delete_drawing_comment(
        session, drawing_id=drawing_id, comment_id=comment_id, author_id=user.id
    )
