from fastapi import APIRouter, File, Form, UploadFile

from app.api.dependencies import CurrentUserDep, DatabaseDep
from app.schemas.drawings import DrawingListSchema, DrawingSchema
from app.services import drawings as service

router = APIRouter()


@router.post("", status_code=201, response_model=DrawingSchema)
async def create_drawing(
    db: DatabaseDep,
    current_user: CurrentUserDep,
    post_code: str = Form(...),
    content: str = Form(...),
    files: list[UploadFile] = File(...),
):
    return service.create_drawing(db, current_user, post_code, content, files)


@router.get("", response_model=DrawingListSchema)
async def get_drawings(
    db: DatabaseDep,
    current_user: CurrentUserDep,
):
    return service.get_drawings(db)


@router.get("/{drawing_code}", response_model=DrawingSchema)
async def get_drawing(
    drawing_code: str,
    db: DatabaseDep,
    current_user: CurrentUserDep,
):
    return service.get_drawing(db, drawing_code)


@router.put("/{drawing_code}", response_model=DrawingSchema)
async def update_drawing(
    drawing_code: str,
    db: DatabaseDep,
    current_user: CurrentUserDep,
    content: str = Form(...),
    files: list[UploadFile] = File(...),
):
    return service.update_drawing(
        db=db,
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
    service.delete_drawing(db=db, code=drawing_code, user=current_user)
