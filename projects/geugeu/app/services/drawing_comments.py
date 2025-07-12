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


class DrawingCommentService:
    def __init__(self, db: Session):
        self.db = db

    def create_comment(
        self,
        *,
        user: User,
        drawing_code: str,
        payload: CreateCommentSchema,
    ) -> CommentSchema:
        drawing = self.db.execute(
            select(Drawing).where(
                Drawing.code == drawing_code,
                Drawing.deleted_at.is_(None),
            )
        ).scalar_one_or_none()
        if not drawing:
            raise HTTPException(status_code=404, detail="Drawing not found")
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
            drawing_id=drawing.id,
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
        drawing_code: str,
    ) -> CommentListSchema:
        drawing = self.db.execute(
            select(Drawing).where(
                Drawing.code == drawing_code,
                Drawing.deleted_at.is_(None),
            )
        ).scalar_one_or_none()
        if not drawing:
            raise HTTPException(status_code=404, detail="Drawing not found")
        comments = (
            self.db.execute(
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
        return CommentListSchema(
            count=len(comments),
            items=[CommentSchema.from_model(comment) for comment in comments],
        )

    def get_comment(
        self,
        *,
        user: User,
        drawing_code: str,
        comment_code: str,
    ) -> CommentSchema:
        drawing = self.db.execute(
            select(Drawing).where(
                Drawing.code == drawing_code,
                Drawing.deleted_at.is_(None),
            )
        ).scalar_one_or_none()
        if not drawing:
            raise HTTPException(status_code=404, detail="Drawing not found")
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
        drawing_code: str,
        comment_code: str,
        payload: UpdateCommentSchema,
    ) -> CommentSchema:
        drawing = self.db.execute(
            select(Drawing).where(
                Drawing.code == drawing_code,
                Drawing.deleted_at.is_(None),
            )
        ).scalar_one_or_none()
        if not drawing:
            raise HTTPException(status_code=404, detail="Drawing not found")
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
        drawing_code: str,
        comment_code: str,
    ) -> None:
        drawing = self.db.execute(
            select(Drawing).where(
                Drawing.code == drawing_code,
                Drawing.deleted_at.is_(None),
            )
        ).scalar_one_or_none()
        if not drawing:
            raise HTTPException(status_code=404, detail="Drawing not found")
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
