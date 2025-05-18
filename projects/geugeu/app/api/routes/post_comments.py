from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.db import get_db
from app.models import User
from app.schemas.post_comments import (
    CommentListSchema,
    CommentSchema,
    CreateCommentSchema,
    UpdateCommentSchema,
)
from app.services import post_comments as service

router = APIRouter()


@router.post("/{post_code}/comments", status_code=201, response_model=CommentSchema)
async def create_comment(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    post_code: str,
    payload: CreateCommentSchema,
):
    return service.create_comment(
        db=session,
        user=current_user,
        post_code=post_code,
        payload=payload,
    )


@router.get("/{post_code}/comments", response_model=CommentListSchema)
async def get_comments(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    post_code: str,
):
    return service.get_comments(
        db=session,
        user=current_user,
        post_code=post_code,
    )


@router.get("/{post_code}/comments/{comment_code}", response_model=CommentSchema)
async def get_comment(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    post_code: str,
    comment_code: str,
):
    return service.get_comment(
        db=session,
        user=current_user,
        post_code=post_code,
        comment_code=comment_code,
    )


@router.put("/{post_code}/comments/{comment_code}", response_model=CommentSchema)
async def update_comment(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    post_code: str,
    comment_code: str,
    payload: UpdateCommentSchema,
):
    return service.update_comment(
        db=session,
        user=current_user,
        post_code=post_code,
        comment_code=comment_code,
        payload=payload,
    )


@router.delete("/{post_code}/comments/{comment_code}", status_code=204)
async def delete_comment(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    post_code: str,
    comment_code: str,
):
    service.delete_comment(
        db=session,
        user=current_user,
        post_code=post_code,
        comment_code=comment_code,
    )
