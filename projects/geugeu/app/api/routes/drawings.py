from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.db import get_db
from app.crud import drawings as crud
from app.models import User
from app.schemas.drawings import DrawingListSchema, DrawingSchema

router = APIRouter()


@router.post("", status_code=201, response_model=DrawingSchema)
async def create_drawing(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    post_code: str = Form(...),
    content: str = Form(...),
    files: list[UploadFile] = File(...),
):
    return crud.create_drawing(session, current_user, post_code, content, files)


@router.get("", response_model=DrawingListSchema)
async def get_drawings(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return crud.get_drawings(session)


@router.get("/{drawing_code}", response_model=DrawingSchema)
async def get_drawing(
    drawing_code: str,
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return crud.get_drawing(session, drawing_code)


@router.put("/{drawing_code}", response_model=DrawingSchema)
async def update_drawing(
    drawing_code: str,
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    content: str = Form(...),
    files: list[UploadFile] = File(...),
):
    return crud.update_drawing(
        session=session,
        user=current_user,
        code=drawing_code,
        content=content,
        files=files,
    )


@router.delete("/{drawing_code}", status_code=204)
async def delete_drawing(
    drawing_code: str,
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    crud.delete_drawing(session=session, code=drawing_code, user=current_user)
