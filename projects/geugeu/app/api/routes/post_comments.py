from fastapi import APIRouter

from app.api.dependencies import CurrentUserDep
from app.core.dependencies import PostCommentServiceDep
from app.schemas.post_comments import (
    CommentListSchema,
    CommentSchema,
    CreateCommentSchema,
    UpdateCommentSchema,
)

router = APIRouter()


@router.post("/{post_code}/comments", status_code=201, response_model=CommentSchema)
async def create_comment(
    post_code: str,
    payload: CreateCommentSchema,
    current_user: CurrentUserDep,
    service: PostCommentServiceDep,
):
    return service.create_comment(
        user=current_user,
        post_code=post_code,
        payload=payload,
    )


@router.get("/{post_code}/comments", response_model=CommentListSchema)
async def get_comments(
    post_code: str,
    current_user: CurrentUserDep,
    service: PostCommentServiceDep,
):
    return service.get_comments(
        user=current_user,
        post_code=post_code,
    )


@router.get("/{post_code}/comments/{comment_code}", response_model=CommentSchema)
async def get_comment(
    post_code: str,
    comment_code: str,
    current_user: CurrentUserDep,
    service: PostCommentServiceDep,
):
    return service.get_comment(
        user=current_user,
        post_code=post_code,
        comment_code=comment_code,
    )


@router.put("/{post_code}/comments/{comment_code}", response_model=CommentSchema)
async def update_comment(
    post_code: str,
    comment_code: str,
    payload: UpdateCommentSchema,
    current_user: CurrentUserDep,
    service: PostCommentServiceDep,
):
    return service.update_comment(
        user=current_user,
        post_code=post_code,
        comment_code=comment_code,
        payload=payload,
    )


@router.delete("/{post_code}/comments/{comment_code}", status_code=204)
async def delete_comment(
    post_code: str,
    comment_code: str,
    current_user: CurrentUserDep,
    service: PostCommentServiceDep,
):
    service.delete_comment(
        user=current_user,
        post_code=post_code,
        comment_code=comment_code,
    )
