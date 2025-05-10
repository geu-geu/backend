from datetime import UTC, datetime

from fastapi import HTTPException, UploadFile
from sqlalchemy import exists, select
from sqlalchemy.orm import Session, joinedload, selectinload, with_loader_criteria

from app.models import Drawing, Image, Post, User
from app.schemas.drawings import DrawingListSchema, DrawingSchema
from app.utils import upload_file


def create_drawing(
    session: Session, user: User, post_code: str, content: str, files: list[UploadFile]
) -> DrawingSchema:
    post = session.execute(
        select(Post).where(
            Post.code == post_code,
            Post.deleted_at.is_(None),
        )
    ).scalar_one()

    if session.execute(
        exists(Drawing.id)
        .where(Drawing.post_id == post.id, Drawing.deleted_at.is_(None))
        .select()
    ).scalar():
        raise HTTPException(status_code=400, detail="Drawing already exists")

    with session.begin_nested():
        drawing = Drawing(post_id=post.id, author_id=user.id, content=content)
        session.add(drawing)
        session.flush()

        images = []
        for file in files:
            image_url = upload_file(file)
            image = Image(drawing_id=drawing.id, url=image_url)
            images.append(image)
        session.add_all(images)

    session.commit()
    return DrawingSchema.from_model(drawing)


def get_drawings(session: Session) -> DrawingListSchema:
    drawings = (
        session.execute(
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
        .scalars()
        .unique()
        .all()
    )
    return DrawingListSchema(
        count=len(drawings),
        items=[DrawingSchema.from_model(drawing) for drawing in drawings],
    )


def get_drawing(session: Session, code: str) -> DrawingSchema:
    drawing = session.execute(
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
    *,
    session: Session,
    user: User,
    code: str,
    content: str,
    files: list[UploadFile],
) -> DrawingSchema:
    drawing = session.execute(
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

    with session.begin_nested():
        # drawing 수정
        drawing.content = content
        session.add(drawing)

        # 기존 drawing images 전부 삭제
        for image in drawing.images:
            image.deleted_at = datetime.now(UTC)
            session.add(image)

        # 새로운 drawing images 생성
        images = []
        for file in files:
            image_url = upload_file(file)
            image = Image(drawing_id=drawing.id, url=image_url)
            images.append(image)
        session.add_all(images)

    session.commit()
    session.refresh(drawing)
    return DrawingSchema.from_model(drawing)


def delete_drawing(*, session: Session, code: str, user: User) -> None:
    drawing = session.execute(
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
    session.commit()
