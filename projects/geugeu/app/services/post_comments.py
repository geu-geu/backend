from datetime import UTC, datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Comment, Post, User
from app.schemas.post_comments import (
    CommentListSchema,
    CommentSchema,
    CreateCommentSchema,
    UpdateCommentSchema,
)


def create_comment(
    *,
    db: Session,
    user: User,
    post_code: str,
    payload: CreateCommentSchema,
) -> CommentSchema:
    post = db.execute(
        select(Post).where(
            Post.code == post_code,
            Post.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if payload.parent_code:
        parent = db.execute(
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
        post_id=post.id,
        author_id=user.id,
        parent_id=parent_id,
        content=payload.content,
    )
    db.add(comment)
    db.commit()
    return CommentSchema.from_model(comment)


def get_comments(
    *,
    db: Session,
    user: User,
    post_code: str,
) -> CommentListSchema:
    post = db.execute(
        select(Post).where(
            Post.code == post_code,
            Post.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comments = (
        db.execute(
            select(Comment)
            .options(joinedload(Comment.author))
            .where(
                Comment.post_id == post.id,
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
    db: Session,
    user: User,
    post_code: str,
    comment_code: str,
) -> CommentSchema:
    post = db.execute(
        select(Post).where(
            Post.code == post_code,
            Post.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comment = db.execute(
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
    db: Session,
    user: User,
    post_code: str,
    comment_code: str,
    payload: UpdateCommentSchema,
) -> CommentSchema:
    post = db.execute(
        select(Post).where(
            Post.code == post_code,
            Post.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comment = db.execute(
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
    db.commit()
    return CommentSchema.from_model(comment)


def delete_comment(
    *,
    db: Session,
    user: User,
    post_code: str,
    comment_code: str,
) -> None:
    post = db.execute(
        select(Post).where(
            Post.code == post_code,
            Post.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comment = db.execute(
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
    db.commit()
