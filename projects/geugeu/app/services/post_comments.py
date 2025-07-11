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


class PostCommentService:
    def __init__(self, db: Session):
        self.db = db

    def create_comment(
        self,
        *,
        user: User,
        post_code: str,
        payload: CreateCommentSchema,
    ) -> CommentSchema:
        post = self.db.execute(
            select(Post).where(
                Post.code == post_code,
                Post.deleted_at.is_(None),
            )
        ).scalar_one_or_none()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        if payload.parent_code:
            parent = self.db.execute(
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
        self.db.add(comment)
        self.db.commit()
        return CommentSchema.from_model(comment)

    def get_comments(
        self,
        *,
        user: User,
        post_code: str,
    ) -> CommentListSchema:
        post = self.db.execute(
            select(Post).where(
                Post.code == post_code,
                Post.deleted_at.is_(None),
            )
        ).scalar_one_or_none()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        comments = (
            self.db.execute(
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
        self,
        *,
        user: User,
        post_code: str,
        comment_code: str,
    ) -> CommentSchema:
        post = self.db.execute(
            select(Post).where(
                Post.code == post_code,
                Post.deleted_at.is_(None),
            )
        ).scalar_one_or_none()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        comment = self.db.execute(
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
        self,
        *,
        user: User,
        post_code: str,
        comment_code: str,
        payload: UpdateCommentSchema,
    ) -> CommentSchema:
        post = self.db.execute(
            select(Post).where(
                Post.code == post_code,
                Post.deleted_at.is_(None),
            )
        ).scalar_one_or_none()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        comment = self.db.execute(
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
            raise HTTPException(status_code=403, detail="Forbidden")
        comment.content = payload.content
        self.db.commit()
        return CommentSchema.from_model(comment)

    def delete_comment(
        self,
        *,
        user: User,
        post_code: str,
        comment_code: str,
    ) -> None:
        post = self.db.execute(
            select(Post).where(
                Post.code == post_code,
                Post.deleted_at.is_(None),
            )
        ).scalar_one_or_none()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        comment = self.db.execute(
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
            raise HTTPException(status_code=403, detail="Forbidden")
        comment.deleted_at = datetime.now(UTC)
        self.db.commit()
