from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.db import get_db
from app.models import User
from app.schemas.drawings import DrawingListSchema, DrawingSchema
from app.services import drawings as service

router = APIRouter()


@router.post("", status_code=201, response_model=DrawingSchema)
async def create_drawing(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    post_code: str = Form(...),
    content: str = Form(...),
    files: list[UploadFile] = File(...),
):
    return service.create_drawing(db, current_user, post_code, content, files)


@router.get("", response_model=DrawingListSchema)
async def get_drawings(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return service.get_drawings(db)


@router.get("/{drawing_code}", response_model=DrawingSchema)
async def get_drawing(
    drawing_code: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return service.get_drawing(db, drawing_code)


@router.put("/{drawing_code}", response_model=DrawingSchema)
async def update_drawing(
    drawing_code: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
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
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    service.delete_drawing(db=db, code=drawing_code, user=current_user)
