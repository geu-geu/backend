from typing import Annotated

from fastapi import APIRouter, File, Form, Query, UploadFile

from app.api.dependencies import CurrentUserDep
from app.core.dependencies import DrawingServiceDep
from app.schemas.drawings import DrawingListFilter, DrawingListSchema, DrawingSchema

router = APIRouter()


@router.post("", status_code=201, response_model=DrawingSchema)
async def create_drawing(
    current_user: CurrentUserDep,
    service: DrawingServiceDep,
    post_code: str = Form(...),
    content: str = Form(...),
    files: list[UploadFile] = File(...),
):
    return service.create_drawing(current_user, post_code, content, files)


@router.get("", response_model=DrawingListSchema)
async def get_drawings(
    current_user: CurrentUserDep,
    service: DrawingServiceDep,
    filters: Annotated[DrawingListFilter, Query()],
):
    return service.get_drawings(filters)


@router.get("/{drawing_code}", response_model=DrawingSchema)
async def get_drawing(
    drawing_code: str,
    current_user: CurrentUserDep,
    service: DrawingServiceDep,
):
    return service.get_drawing(drawing_code)


@router.put("/{drawing_code}", response_model=DrawingSchema)
async def update_drawing(
    drawing_code: str,
    current_user: CurrentUserDep,
    service: DrawingServiceDep,
    content: str = Form(...),
    files: list[UploadFile] = File(...),
):
    return service.update_drawing(
        user=current_user,
        code=drawing_code,
        content=content,
        files=files,
    )


@router.delete("/{drawing_code}", status_code=204)
async def delete_drawing(
    drawing_code: str,
    current_user: CurrentUserDep,
    service: DrawingServiceDep,
):
    service.delete_drawing(code=drawing_code, user=current_user)
