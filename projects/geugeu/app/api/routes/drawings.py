from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.db import get_db
from app.crud import drawings as crud
from app.models import User
from app.schemas.drawings import (
    CreateDrawingSchema,
    DrawingListSchema,
    DrawingSchema,
    UpdateDrawingSchema,
)

router = APIRouter()


@router.post("", status_code=201, response_model=DrawingSchema)
async def create_drawing(
    payload: CreateDrawingSchema,
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return crud.create_drawing(session, current_user, payload)


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
    payload: UpdateDrawingSchema,
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return crud.update_drawing(
        session=session,
        code=drawing_code,
        payload=payload,
        user=current_user,
    )


@router.delete("/{drawing_code}", status_code=204)
async def delete_drawing(
    drawing_code: str,
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    crud.delete_drawing(session=session, code=drawing_code, user=current_user)
