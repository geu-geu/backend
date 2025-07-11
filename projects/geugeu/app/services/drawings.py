from datetime import UTC, datetime

from fastapi import HTTPException, UploadFile
from sqlalchemy import exists, func, select
from sqlalchemy.orm import Session, joinedload, selectinload, with_loader_criteria

from app.models import Drawing, Image, Post, User
from app.schemas.drawings import DrawingListFilter, DrawingListSchema, DrawingSchema
from app.utils import upload_file


class DrawingService:
    def __init__(self, db: Session):
        self.db = db

    def create_drawing(
        self, user: User, post_code: str, content: str, files: list[UploadFile]
    ) -> DrawingSchema:
        post = self.db.execute(
            select(Post).where(
                Post.code == post_code,
                Post.deleted_at.is_(None),
            )
        ).scalar_one()

        if self.db.execute(
            exists(Drawing.id)
            .where(Drawing.post_id == post.id, Drawing.deleted_at.is_(None))
            .select()
        ).scalar():
            raise HTTPException(status_code=400, detail="Drawing already exists")

        with self.db.begin_nested():
            drawing = Drawing(post_id=post.id, author_id=user.id, content=content)
            self.db.add(drawing)
            self.db.flush()

            images = []
            for file in files:
                image_url = upload_file(file)
                image = Image(drawing_id=drawing.id, url=image_url)
                images.append(image)
            self.db.add_all(images)

        self.db.commit()
        return DrawingSchema.from_model(drawing)

    def get_drawings(self, filters: DrawingListFilter) -> DrawingListSchema:
        stmt = (
            select(Drawing)
            .options(
                joinedload(Drawing.post),
                joinedload(Drawing.author),
                selectinload(Drawing.images),
                with_loader_criteria(Image, Image.deleted_at.is_(None)),
            )
            .where(Drawing.deleted_at.is_(None))
            .order_by(Drawing.id.desc())
        )

        if filters.post_code:
            stmt = stmt.join(Post, Drawing.post_id == Post.id).where(
                Post.code == filters.post_code
            )

        if filters.author_code:
            stmt = stmt.join(User, Drawing.author_id == User.id).where(
                User.code == filters.author_code
            )

        offset = (filters.page - 1) * filters.page_size
        count = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()
        rows = (
            self.db.execute(stmt.offset(offset).limit(filters.page_size))
            .scalars()
            .all()
        )
        return DrawingListSchema(
            count=count,
            items=[DrawingSchema.from_model(row) for row in rows],
        )

    def get_drawing(self, code: str) -> DrawingSchema:
        drawing = self.db.execute(
            select(Drawing)
            .options(
                joinedload(Drawing.post),
                joinedload(Drawing.author),
                selectinload(Drawing.images),
                with_loader_criteria(Image, Image.deleted_at.is_(None)),
            )
            .where(
                Drawing.code == code,
                Drawing.deleted_at.is_(None),
            )
        ).scalar_one_or_none()
        if drawing is None:
            raise HTTPException(status_code=404, detail="Drawing not found")
        return DrawingSchema.from_model(drawing)

    def update_drawing(
        self,
        *,
        user: User,
        code: str,
        content: str,
        files: list[UploadFile],
    ) -> DrawingSchema:
        drawing = self.db.execute(
            select(Drawing)
            .options(
                joinedload(Drawing.post),
                joinedload(Drawing.author),
                selectinload(Drawing.images),
                with_loader_criteria(Image, Image.deleted_at.is_(None)),
            )
            .where(
                Drawing.code == code,
                Drawing.deleted_at.is_(None),
            )
        ).scalar_one_or_none()
        if drawing is None:
            raise HTTPException(status_code=404, detail="Drawing not found")
        if drawing.author_id == user.id or user.is_admin:
            pass
        else:
            raise HTTPException(status_code=403, detail="Forbidden")

        with self.db.begin_nested():
            # drawing 수정
            drawing.content = content
            self.db.add(drawing)

            # 기존 drawing images 전부 삭제
            for image in drawing.images:
                image.deleted_at = datetime.now(UTC)
                self.db.add(image)

            # 새로운 drawing images 생성
            images = []
            for file in files:
                image_url = upload_file(file)
                image = Image(drawing_id=drawing.id, url=image_url)
                images.append(image)
            self.db.add_all(images)

        self.db.commit()
        self.db.refresh(drawing)
        return DrawingSchema.from_model(drawing)

    def delete_drawing(self, *, code: str, user: User) -> None:
        drawing = self.db.execute(
            select(Drawing).where(
                Drawing.code == code,
                Drawing.deleted_at.is_(None),
            )
        ).scalar_one_or_none()
        if drawing is None:
            raise HTTPException(status_code=404, detail="Drawing not found")
        if drawing.author_id == user.id or user.is_admin:
            pass
        else:
            raise HTTPException(status_code=403, detail="Forbidden")
        drawing.deleted_at = datetime.now(UTC)
        self.db.commit()
