from fastapi import APIRouter

from app.api.dependencies import CurrentUserDep, DatabaseDep
from app.schemas.drawing_comments import (
    CommentListSchema,
    CommentSchema,
    CreateCommentSchema,
    UpdateCommentSchema,
)
from app.services import drawing_comments as service

router = APIRouter()


@router.post(
    "/{drawing_code}/comments",
    status_code=201,
    response_model=CommentSchema,
)
async def create_comment(
    db: DatabaseDep,
    current_user: CurrentUserDep,
    drawing_code: str,
    payload: CreateCommentSchema,
):
    return service.create_comment(
        db=db,
        user=current_user,
        drawing_code=drawing_code,
        payload=payload,
    )


@router.get("/{drawing_code}/comments", response_model=CommentListSchema)
async def get_comments(
    db: DatabaseDep,
    current_user: CurrentUserDep,
    drawing_code: str,
):
    return service.get_comments(
        db=db,
        user=current_user,
        drawing_code=drawing_code,
    )


@router.get(
    "/{drawing_code}/comments/{comment_code}",
    response_model=CommentSchema,
)
async def get_comment(
    db: DatabaseDep,
    current_user: CurrentUserDep,
    drawing_code: str,
    comment_code: str,
):
    return service.get_comment(
        db=db,
        user=current_user,
        drawing_code=drawing_code,
        comment_code=comment_code,
    )


@router.put("/{drawing_code}/comments/{comment_code}", response_model=CommentSchema)
async def update_comment(
    db: DatabaseDep,
    current_user: CurrentUserDep,
    drawing_code: str,
    comment_code: str,
    payload: UpdateCommentSchema,
):
    return service.update_comment(
        db=db,
        user=current_user,
        drawing_code=drawing_code,
        comment_code=comment_code,
        payload=payload,
    )


@router.delete("/{drawing_code}/comments/{comment_code}", status_code=204)
async def delete_comment(
    db: DatabaseDep,
    current_user: CurrentUserDep,
    drawing_code: str,
    comment_code: str,
):
    service.delete_comment(
        db=db,
        user=current_user,
        drawing_code=drawing_code,
        comment_code=comment_code,
    )
