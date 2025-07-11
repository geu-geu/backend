from typing import Annotated

from fastapi import APIRouter, File, Form, Query, UploadFile

from app.api.dependencies import CurrentUserDep, DatabaseDep
from app.schemas.drawings import DrawingListFilter, DrawingListSchema, DrawingSchema
from app.services.drawings import DrawingService

router = APIRouter()


@router.post("", status_code=201, response_model=DrawingSchema)
async def create_drawing(
    db: DatabaseDep,
    current_user: CurrentUserDep,
    post_code: str = Form(...),
    content: str = Form(...),
    files: list[UploadFile] = File(...),
):
    service = DrawingService(db)
    return service.create_drawing(current_user, post_code, content, files)


@router.get("", response_model=DrawingListSchema)
async def get_drawings(
    db: DatabaseDep,
    current_user: CurrentUserDep,
    filters: Annotated[DrawingListFilter, Query()],
):
    service = DrawingService(db)
    return service.get_drawings(filters)


@router.get("/{drawing_code}", response_model=DrawingSchema)
async def get_drawing(
    drawing_code: str,
    db: DatabaseDep,
    current_user: CurrentUserDep,
):
    service = DrawingService(db)
    return service.get_drawing(drawing_code)


@router.put("/{drawing_code}", response_model=DrawingSchema)
async def update_drawing(
    drawing_code: str,
    db: DatabaseDep,
    current_user: CurrentUserDep,
    content: str = Form(...),
    files: list[UploadFile] = File(...),
):
    service = DrawingService(db)
    return service.update_drawing(
        user=current_user,
        code=drawing_code,
        content=content,
        files=files,
    )


@router.delete("/{drawing_code}", status_code=204)
async def delete_drawing(
    drawing_code: str,
    db: DatabaseDep,
    current_user: CurrentUserDep,
):
    service = DrawingService(db)
    service.delete_drawing(code=drawing_code, user=current_user)
