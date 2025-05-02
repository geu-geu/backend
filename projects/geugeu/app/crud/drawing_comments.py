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
    UserSchema,
)


def create_comment(
    *,
    session: Session,
    user: User,
    drawing_code: str,
    schema: CreateCommentSchema,
) -> CommentSchema:
    drawing = session.execute(
        select(Drawing).where(
            Drawing.code == drawing_code,
            Drawing.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if not drawing:
        raise HTTPException(status_code=404, detail="Drawing not found")
    comment = Comment(
        drawing_id=drawing.id,
        author_id=user.id,
        content=schema.content,
    )
    session.add(comment)
    session.commit()
    return CommentSchema(
        code=comment.code,
        author=UserSchema(
            code=user.code,
            email=user.email,
            nickname=user.nickname,
            profile_image_url=user.profile_image_url,
        ),
        content=comment.content,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
    )


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
                Comment.deleted_at.is_(None),
            )
        )
        .scalars()
        .all()
    )
    items = []
    for comment in comments:
        item = CommentSchema(
            code=comment.code,
            author=UserSchema(
                code=comment.author.code,
                email=comment.author.email,
                nickname=comment.author.nickname,
                profile_image_url=comment.author.profile_image_url,
            ),
            content=comment.content,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )
        items.append(item)
    return CommentListSchema(
        count=len(comments),
        items=items,
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
    return CommentSchema(
        code=comment.code,
        author=UserSchema(
            code=comment.author.code,
            email=comment.author.email,
            nickname=comment.author.nickname,
            profile_image_url=comment.author.profile_image_url,
        ),
        content=comment.content,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
    )


def update_comment(
    *,
    session: Session,
    user: User,
    drawing_code: str,
    comment_code: str,
    schema: UpdateCommentSchema,
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
    comment.content = schema.content
    session.commit()
    return CommentSchema(
        code=comment.code,
        author=UserSchema(
            code=comment.author.code,
            email=comment.author.email,
            nickname=comment.author.nickname,
            profile_image_url=comment.author.profile_image_url,
        ),
        content=comment.content,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
    )


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
