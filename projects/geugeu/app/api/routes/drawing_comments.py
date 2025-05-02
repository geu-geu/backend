from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.crud import drawing_comments as crud
from app.models import User
from app.schemas.drawing_comments import CreateCommentSchema, UpdateCommentSchema

router = APIRouter()


@router.post("/{drawing_code}/comments", status_code=201)
async def create_comment(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    drawing_code: str,
    schema: CreateCommentSchema,
):
    return crud.create_comment(
        session=session,
        user=current_user,
        drawing_code=drawing_code,
        schema=schema,
    )


@router.get("/{drawing_code}/comments")
async def get_comments(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    drawing_code: str,
):
    return crud.get_comments(
        session=session,
        user=current_user,
        drawing_code=drawing_code,
    )


@router.get("/{drawing_code}/comments/{comment_code}")
async def get_comment(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    drawing_code: str,
    comment_code: str,
):
    return crud.get_comment(
        session=session,
        user=current_user,
        drawing_code=drawing_code,
        comment_code=comment_code,
    )


@router.put("/{drawing_code}/comments/{comment_code}")
async def update_comment(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    drawing_code: str,
    comment_code: str,
    schema: UpdateCommentSchema,
):
    return crud.update_comment(
        session=session,
        user=current_user,
        drawing_code=drawing_code,
        comment_code=comment_code,
        schema=schema,
    )


@router.delete("/{drawing_code}/comments/{comment_code}", status_code=204)
async def delete_comment(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    drawing_code: str,
    comment_code: str,
):
    crud.delete_comment(
        session=session,
        user=current_user,
        drawing_code=drawing_code,
        comment_code=comment_code,
    )
