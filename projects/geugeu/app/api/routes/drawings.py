from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.db import get_db
from app.crud import drawings as crud
from app.models import User
from app.schemas.drawings import CreateDrawingSchema, UpdateDrawingSchema

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
async def update_drawing(
    drawing_code: str,
    schema: UpdateDrawingSchema,
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return crud.update_drawing(
        session=session,
        code=drawing_code,
        schema=schema,
        user=current_user,
    )


@router.delete("/{drawing_code}", status_code=204)
async def delete_drawing(
    drawing_code: str,
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    crud.delete_drawing(session=session, code=drawing_code, user=current_user)
