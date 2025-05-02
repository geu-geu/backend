from datetime import UTC, datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Comment, Post, User
from app.schemas.post_comments import (
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
    comment = Comment(
        post_id=post.id,
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
            select(Comment).where(
                Comment.post_id == post.id,
                Comment.deleted_at.is_(None),
            )
        )
        .scalars()
        .all()
    )
    items = []
    for comment in comments:
        author = session.execute(
            select(User).where(User.id == comment.author_id)
        ).scalar_one()
        item = CommentSchema(
            code=comment.code,
            author=UserSchema(
                code=author.code,
                email=author.email,
                nickname=author.nickname,
                profile_image_url=author.profile_image_url,
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
        select(Comment).where(
            Comment.code == comment_code,
            Comment.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    author = session.execute(
        select(User).where(User.id == comment.author_id)
    ).scalar_one()
    return CommentSchema(
        code=comment.code,
        author=UserSchema(
            code=author.code,
            email=author.email,
            nickname=author.nickname,
            profile_image_url=author.profile_image_url,
        ),
        content=comment.content,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
    )


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
    comment.content = schema.content
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
