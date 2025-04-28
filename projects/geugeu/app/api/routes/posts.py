from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.dependencies import get_current_user
from app.core.db import get_db
from app.crud import posts as crud
from app.models import User
from app.schemas.posts import CreatePostSchema

router = APIRouter()


@router.post("", status_code=201)
async def create_post(
    schema: CreatePostSchema,
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return crud.create_post(session, current_user, schema)


@router.get("")
async def get_posts():
    raise NotImplementedError


@router.get("/{post_code}")
async def get_post(post_code: str):
    raise NotImplementedError


@router.put("/{post_code}")
async def update_post(post_code: str):
    raise NotImplementedError


@router.delete("/{post_code}")
async def delete_post(post_code: str):
    raise NotImplementedError
