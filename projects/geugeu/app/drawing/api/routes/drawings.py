from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status
from ulid import ULID

from app.auth.deps import CurrentUserDep
from app.database import SessionDep
from app.drawing.api.schemas.drawings import (
    CompleteDrawingBody,
    CreateDrawingBody,
    DrawingResponse,
    UpdateDrawingBody,
)
from app.drawing.deps import drawing_service
from app.drawing.domain.drawing import Drawing, DrawingStatus
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
        session, drawing=drawing, image_urls=body.image_urls
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
