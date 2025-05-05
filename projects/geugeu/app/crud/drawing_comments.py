from datetime import UTC, datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Comment, Drawing, User
from app.schemas.drawing_comments import (
    CommentListSchema,
    CommentSchema,
    CreateCommentSchema,
    UpdateCommentSchema,
)


def create_comment(
    *,
    session: Session,
    user: User,
    drawing_code: str,
    payload: CreateCommentSchema,
) -> CommentSchema:
    drawing = session.execute(
        select(Drawing).where(
            Drawing.code == drawing_code,
            Drawing.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if not drawing:
        raise HTTPException(status_code=404, detail="Drawing not found")
    if payload.parent_code:
        parent = session.execute(
            select(Comment).where(
                Comment.code == payload.parent_code,
                Comment.deleted_at.is_(None),
            )
        ).scalar_one_or_none()
        if not parent:
            raise HTTPException(status_code=400, detail="Invalid parent code")
        parent_id = parent.id
    else:
        parent_id = None
    comment = Comment(
        drawing_id=drawing.id,
        author_id=user.id,
        parent_id=parent_id,
        content=payload.content,
    )
    session.add(comment)
    session.commit()
    return CommentSchema.from_model(comment)


def get_comments(
    *,
    session: Session,
    user: User,
    drawing_code: str,
) -> CommentListSchema:
    drawing = session.execute(
        select(Drawing).where(
            Drawing.code == drawing_code,
            Drawing.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if not drawing:
        raise HTTPException(status_code=404, detail="Drawing not found")
    comments = (
        session.execute(
            select(Comment)
            .options(joinedload(Comment.author))
            .where(
                Comment.drawing_id == drawing.id,
                Comment.parent_id.is_(None),
                Comment.deleted_at.is_(None),
            )
        )
        .scalars()
        .all()
    )
    return CommentListSchema(
        count=len(comments),
        items=[CommentSchema.from_model(comment) for comment in comments],
    )


def get_comment(
    *,
    session: Session,
    user: User,
    drawing_code: str,
    comment_code: str,
) -> CommentSchema:
    drawing = session.execute(
        select(Drawing).where(
            Drawing.code == drawing_code,
            Drawing.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if not drawing:
        raise HTTPException(status_code=404, detail="Drawing not found")
    comment = session.execute(
        select(Comment)
        .options(joinedload(Comment.author))
        .where(
            Comment.code == comment_code,
            Comment.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return CommentSchema.from_model(comment)


def update_comment(
    *,
    session: Session,
    user: User,
    drawing_code: str,
    comment_code: str,
    payload: UpdateCommentSchema,
) -> CommentSchema:
    drawing = session.execute(
        select(Drawing).where(
            Drawing.code == drawing_code,
            Drawing.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if not drawing:
        raise HTTPException(status_code=404, detail="Drawing not found")
    comment = session.execute(
        select(Comment)
        .options(joinedload(Comment.author))
        .where(
            Comment.code == comment_code,
            Comment.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id == user.id or user.is_admin:
        pass
    else:
        raise HTTPException(status_code=403, detail="Forbiden")
    comment.content = payload.content
    session.commit()
    return CommentSchema.from_model(comment)


def delete_comment(
    *,
    session: Session,
    user: User,
    drawing_code: str,
    comment_code: str,
) -> None:
    drawing = session.execute(
        select(Drawing).where(
            Drawing.code == drawing_code,
            Drawing.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if not drawing:
        raise HTTPException(status_code=404, detail="Drawing not found")
    comment = session.execute(
        select(Comment).where(
            Comment.code == comment_code,
            Comment.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id == user.id or user.is_admin:
        pass
    else:
        raise HTTPException(status_code=403, detail="Forbiden")
    comment.deleted_at = datetime.now(UTC)
    session.commit()
