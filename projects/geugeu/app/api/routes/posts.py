from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.db import get_db
from app.crud import posts as crud
from app.models import User
from app.schemas.posts import (
    CreatePostSchema,
    PostListSchema,
    PostSchema,
    UpdatePostSchema,
)

router = APIRouter()


@router.post("", status_code=201, response_model=PostSchema)
async def create_post(
    schema: CreatePostSchema,
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return crud.create_post(session, current_user, schema)


@router.get("", response_model=PostListSchema)
async def get_posts(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return crud.get_posts(session)


@router.get("/{post_code}", response_model=PostSchema)
async def get_post(
    post_code: str,
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return crud.get_post(session, post_code)


@router.put("/{post_code}", response_model=PostSchema)
async def update_post(
    post_code: str,
    schema: UpdatePostSchema,
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return crud.update_post(
        session=session, code=post_code, schema=schema, user=current_user
    )


@router.delete("/{post_code}", status_code=204)
async def delete_post(
    post_code: str,
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    crud.delete_post(session=session, code=post_code, user=current_user)
