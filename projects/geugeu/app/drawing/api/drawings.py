from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from ulid import ULID

from app.auth.dependencies import CurrentActiveUserDep
from app.drawing.application.drawing_service import DrawingService
from app.drawing.dependencies import drawing_service
from app.drawing.domain.drawing import Drawing

router = APIRouter(prefix="/drawings", tags=["drawings"])


class CreateDrawingBody(BaseModel):
    post_id: str
    content: str
    image_urls: list[str] = Field(default_factory=list)


class UpdateDrawingBody(BaseModel):
    content: str
    image_urls: list[str] = Field(default_factory=list)


class DrawingResponse(BaseModel):
    id: str
    post_id: str
    content: str
    images: list[str]
    created_at: datetime
    updated_at: datetime


@router.get("/by-post/{post_id}", response_model=list[DrawingResponse])
async def get_drawings_by_post_id(
    post_id: str,
    drawing_service: Annotated[DrawingService, Depends(drawing_service)],
) -> list[DrawingResponse]:
    drawings_with_images = drawing_service.get_drawings_by_post_id(post_id=post_id)
    return [
        DrawingResponse(
            id=drawing.id,
            post_id=drawing.post_id,
            content=drawing.content,
            images=[image.image_url for image in images],
            created_at=drawing.created_at,
            updated_at=drawing.updated_at,
        )
        for drawing, images in drawings_with_images
    ]


@router.post("/", response_model=DrawingResponse, status_code=status.HTTP_201_CREATED)
async def create_drawing(
    body: CreateDrawingBody,
    drawing_service: Annotated[DrawingService, Depends(drawing_service)],
    user: CurrentActiveUserDep,
) -> DrawingResponse:
    drawing = Drawing(
        id=str(ULID()),
        post_id=body.post_id,
        author_id=user.id,
        content=body.content,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing, images = drawing_service.create_drawing(
        drawing=drawing, image_urls=body.image_urls
    )
    return DrawingResponse(
        id=drawing.id,
        post_id=drawing.post_id,
        content=drawing.content,
        images=[image.image_url for image in images],
        created_at=drawing.created_at,
        updated_at=drawing.updated_at,
    )


@router.get("/{drawing_id}", response_model=DrawingResponse)
async def get_drawing(
    drawing_id: str,
    drawing_service: Annotated[DrawingService, Depends(drawing_service)],
) -> DrawingResponse:
    drawing, images = drawing_service.get_drawing(drawing_id=drawing_id)
    return DrawingResponse(
        id=drawing.id,
        post_id=drawing.post_id,
        content=drawing.content,
        images=[image.image_url for image in images],
        created_at=drawing.created_at,
        updated_at=drawing.updated_at,
    )


@router.put("/{drawing_id}", response_model=DrawingResponse)
async def update_drawing(
    drawing_id: str,
    body: UpdateDrawingBody,
    drawing_service: Annotated[DrawingService, Depends(drawing_service)],
) -> DrawingResponse:
    drawing, images = drawing_service.update_drawing(
        drawing_id=drawing_id,
        content=body.content,
        image_urls=body.image_urls,
    )
    return DrawingResponse(
        id=drawing.id,
        post_id=drawing.post_id,
        content=drawing.content,
        images=[image.image_url for image in images],
        created_at=drawing.created_at,
        updated_at=drawing.updated_at,
    )


@router.delete("/{drawing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_drawing(
    drawing_id: str,
    drawing_service: Annotated[DrawingService, Depends(drawing_service)],
) -> None:
    drawing_service.delete_drawing(drawing_id=drawing_id)
