from fastapi import APIRouter

from app.api.dependencies import CurrentUserDep
from app.core.dependencies import DrawingCommentServiceDep
from app.schemas.drawing_comments import (
    CommentListSchema,
    CommentSchema,
    CreateCommentSchema,
    UpdateCommentSchema,
)

router = APIRouter()


@router.post(
    "/{drawing_code}/comments",
    status_code=201,
    response_model=CommentSchema,
)
async def create_comment(
    drawing_code: str,
    payload: CreateCommentSchema,
    current_user: CurrentUserDep,
    service: DrawingCommentServiceDep,
):
    return service.create_comment(
        user=current_user,
        drawing_code=drawing_code,
        payload=payload,
    )


@router.get("/{drawing_code}/comments", response_model=CommentListSchema)
async def get_comments(
    drawing_code: str,
    current_user: CurrentUserDep,
    service: DrawingCommentServiceDep,
):
    return service.get_comments(
        user=current_user,
        drawing_code=drawing_code,
    )


@router.get(
    "/{drawing_code}/comments/{comment_code}",
    response_model=CommentSchema,
)
async def get_comment(
    drawing_code: str,
    comment_code: str,
    current_user: CurrentUserDep,
    service: DrawingCommentServiceDep,
):
    return service.get_comment(
        user=current_user,
        drawing_code=drawing_code,
        comment_code=comment_code,
    )


@router.put("/{drawing_code}/comments/{comment_code}", response_model=CommentSchema)
async def update_comment(
    drawing_code: str,
    comment_code: str,
    payload: UpdateCommentSchema,
    current_user: CurrentUserDep,
    service: DrawingCommentServiceDep,
):
    return service.update_comment(
        user=current_user,
        drawing_code=drawing_code,
        comment_code=comment_code,
        payload=payload,
    )


@router.delete("/{drawing_code}/comments/{comment_code}", status_code=204)
async def delete_comment(
    drawing_code: str,
    comment_code: str,
    current_user: CurrentUserDep,
    service: DrawingCommentServiceDep,
):
    service.delete_comment(
        user=current_user,
        drawing_code=drawing_code,
        comment_code=comment_code,
    )
