from datetime import UTC, datetime

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.models import Interest, Post, User
from app.schemas.interests import (
    InterestListSchema,
    InterestResponseSchema,
    InterestSchema,
)


class InterestService:
    def __init__(self, db: Session):
        self.db = db

    def toggle_interest(self, user: User, post_code: str) -> InterestResponseSchema:
        # Find the post
        post = self.db.execute(
            select(Post).where(
                Post.code == post_code,
                Post.deleted_at.is_(None),
            )
        ).scalar_one_or_none()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        # Check if interest already exists
        existing_interest = self.db.execute(
            select(Interest).where(
                Interest.user_id == user.id,
                Interest.post_id == post.id,
                Interest.deleted_at.is_(None),
            )
        ).scalar_one_or_none()

        if existing_interest:
            # Remove interest (soft delete)
            existing_interest.deleted_at = datetime.now(UTC)
            self.db.commit()
            return InterestResponseSchema(
                success=True,
                message="Interest removed successfully",
                is_interested=False,
            )
        else:
            # Add interest
            interest = Interest(user_id=user.id, post_id=post.id)
            self.db.add(interest)
            self.db.commit()
            return InterestResponseSchema(
                success=True,
                message="Interest added successfully",
                is_interested=True,
            )

    def get_post_interests(
        self, post_code: str, current_user: User | None, page: int, page_size: int
    ) -> InterestListSchema:
        # Find the post
        post = self.db.execute(
            select(Post).where(
                Post.code == post_code,
                Post.deleted_at.is_(None),
            )
        ).scalar_one_or_none()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        # Base query for interests
        stmt = (
            select(Interest)
            .options(
                joinedload(Interest.user),
                joinedload(Interest.post),
            )
            .where(
                Interest.post_id == post.id,
                Interest.deleted_at.is_(None),
            )
            .order_by(Interest.created_at.desc())
        )

        # Count total
        count = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()

        # Prepare response
        result = InterestListSchema(
            items=[],
            count=count,
        )

        # Add is_interested only if user is authenticated
        if current_user:
            existing_interest = self.db.execute(
                select(Interest).where(
                    Interest.user_id == current_user.id,
                    Interest.post_id == post.id,
                    Interest.deleted_at.is_(None),
                )
            ).scalar_one_or_none()
            result.is_interested = existing_interest is not None

        # Return early if page_size is 0 (summary only)
        if page_size == 0:
            return result

        # Get paginated results
        offset = (page - 1) * page_size
        interests = (
            self.db.execute(stmt.offset(offset).limit(page_size)).scalars().all()
        )

        result.items = [InterestSchema.from_model(interest) for interest in interests]
        return result

    def get_user_interests(
        self, user_code: str, page: int, page_size: int
    ) -> InterestListSchema:
        # Find the user
        user = self.db.execute(
            select(User).where(
                User.code == user_code,
                User.deleted_at.is_(None),
            )
        ).scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Base query for interests
        stmt = (
            select(Interest)
            .options(
                joinedload(Interest.user),
                joinedload(Interest.post).joinedload(Post.author),
            )
            .where(
                Interest.user_id == user.id,
                Interest.deleted_at.is_(None),
            )
            .order_by(Interest.created_at.desc())
        )

        # Count total
        count = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()

        # Get paginated results
        offset = (page - 1) * page_size
        interests = (
            self.db.execute(stmt.offset(offset).limit(page_size)).scalars().all()
        )

        return InterestListSchema(
            items=[InterestSchema.from_model(interest) for interest in interests],
            count=count,
            # No is_interested field for user interests endpoint
        )
