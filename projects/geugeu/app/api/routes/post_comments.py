from fastapi import APIRouter

from app.api.dependencies import CurrentUserDep, DatabaseDep
from app.schemas.post_comments import (
    CommentListSchema,
    CommentSchema,
    CreateCommentSchema,
    UpdateCommentSchema,
)
from app.services.post_comments import PostCommentService

router = APIRouter()


@router.post("/{post_code}/comments", status_code=201, response_model=CommentSchema)
async def create_comment(
    db: DatabaseDep,
    current_user: CurrentUserDep,
    post_code: str,
    payload: CreateCommentSchema,
):
    service = PostCommentService(db)
    return service.create_comment(
        user=current_user,
        post_code=post_code,
        payload=payload,
    )


@router.get("/{post_code}/comments", response_model=CommentListSchema)
async def get_comments(
    db: DatabaseDep,
    current_user: CurrentUserDep,
    post_code: str,
):
    service = PostCommentService(db)
    return service.get_comments(
        user=current_user,
        post_code=post_code,
    )


@router.get("/{post_code}/comments/{comment_code}", response_model=CommentSchema)
async def get_comment(
    db: DatabaseDep,
    current_user: CurrentUserDep,
    post_code: str,
    comment_code: str,
):
    service = PostCommentService(db)
    return service.get_comment(
        user=current_user,
        post_code=post_code,
        comment_code=comment_code,
    )


@router.put("/{post_code}/comments/{comment_code}", response_model=CommentSchema)
async def update_comment(
    db: DatabaseDep,
    current_user: CurrentUserDep,
    post_code: str,
    comment_code: str,
    payload: UpdateCommentSchema,
):
    service = PostCommentService(db)
    return service.update_comment(
        user=current_user,
        post_code=post_code,
        comment_code=comment_code,
        payload=payload,
    )


@router.delete("/{post_code}/comments/{comment_code}", status_code=204)
async def delete_comment(
    db: DatabaseDep,
    current_user: CurrentUserDep,
    post_code: str,
    comment_code: str,
):
    service = PostCommentService(db)
    service.delete_comment(
        user=current_user,
        post_code=post_code,
        comment_code=comment_code,
    )
