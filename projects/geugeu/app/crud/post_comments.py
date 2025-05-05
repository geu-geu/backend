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
    session: Session,
    user: User,
    post_code: str,
    schema: CreateCommentSchema,
) -> CommentSchema:
    post = session.execute(
        select(Post).where(
            Post.code == post_code,
            Post.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if schema.parent_code:
        parent = session.execute(
            select(Comment).where(
                Comment.code == schema.parent_code,
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
        content=schema.content,
    )
    session.add(comment)
    session.commit()
    return CommentSchema.from_model(comment)


def get_comments(
    *,
    session: Session,
    user: User,
    post_code: str,
) -> CommentListSchema:
    post = session.execute(
        select(Post).where(
            Post.code == post_code,
            Post.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comments = (
        session.execute(
            select(Comment)
            .options(joinedload(Comment.author))
            .where(
                Comment.post_id == post.id,
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
    post_code: str,
    comment_code: str,
) -> CommentSchema:
    post = session.execute(
        select(Post).where(
            Post.code == post_code,
            Post.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
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
    post_code: str,
    comment_code: str,
    schema: UpdateCommentSchema,
) -> CommentSchema:
    post = session.execute(
        select(Post).where(
            Post.code == post_code,
            Post.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
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
    comment.content = schema.content
    session.commit()
    return CommentSchema.from_model(comment)


def delete_comment(
    *,
    session: Session,
    user: User,
    post_code: str,
    comment_code: str,
) -> None:
    post = session.execute(
        select(Post).where(
            Post.code == post_code,
            Post.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
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
