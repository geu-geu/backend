from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.dependencies import get_current_user
from app.core.db import get_db
from app.crud import drawings as crud
from app.models import User
from app.schemas.drawings import CreateDrawingSchema

router = APIRouter()


@router.post("", status_code=201)
async def create_drawing(
    schema: CreateDrawingSchema,
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return crud.create_drawing(session, current_user, schema)


@router.get("")
async def get_drawings(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return crud.get_drawings(session)


@router.get("/{drawing_code}")
async def get_drawing(
    drawing_code: str,
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return crud.get_drawing(session, drawing_code)


@router.put("/{drawing_code}")
async def update_drawing(drawing_code: str):
    raise NotImplementedError


@router.delete("/{drawing_code}")
async def delete_drawing(drawing_code: str):
    raise NotImplementedError
