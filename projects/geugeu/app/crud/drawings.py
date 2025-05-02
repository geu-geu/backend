from datetime import UTC, datetime

from fastapi import HTTPException
from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from app.models import Drawing, Image, Post, User
from app.schemas.drawings import (
    CreateDrawingSchema,
    DrawingListSchema,
    DrawingSchema,
    PostSchema,
    UpdateDrawingSchema,
    UserSchema,
)


def create_drawing(
    session: Session, user: User, schema: CreateDrawingSchema
) -> DrawingSchema:
    post = session.execute(
        select(Post).where(
            Post.code == schema.post_code,
            Post.deleted_at.is_(None),
        )
    ).scalar_one()

    if session.execute(
        exists(Drawing.id)
        .where(Drawing.post_id == post.id, Drawing.deleted_at.is_(None))
        .select()
    ).scalar():
        raise HTTPException(status_code=400, detail="Drawing already exists")

    drawing = Drawing(post_id=post.id, author_id=user.id, content=schema.content)
    session.add(drawing)
    session.commit()

    images = []
    for image_url in schema.image_urls:
        image = Image(drawing_id=drawing.id, url=image_url)
        images.append(image)
    session.add_all(images)
    session.commit()

    return DrawingSchema(
        code=drawing.code,
        post=PostSchema(code=post.code),
        author=UserSchema(
            code=user.code,
            email=user.email,
            nickname=user.nickname,
            profile_image_url=user.profile_image_url,
        ),
        content=drawing.content,
        image_urls=[image.url for image in images],
        created_at=drawing.created_at,
        updated_at=drawing.updated_at,
    )


def get_drawings(session: Session) -> DrawingListSchema:
    drawings = (
        session.execute(select(Drawing).order_by(Drawing.id.desc())).scalars().all()
    )
    results = []
    for drawing in drawings:
        post = session.execute(
            select(Post).where(
                Post.id == drawing.post_id,
                Post.deleted_at.is_(None),
            )
        ).scalar_one()
        author = session.execute(
            select(User).where(
                User.id == drawing.author_id,
                User.deleted_at.is_(None),
            )
        ).scalar_one()
        images = (
            session.execute(
                select(Image).where(
                    Image.drawing_id == drawing.id,
                    Image.deleted_at.is_(None),
                )
            )
            .scalars()
            .all()
        )
        result = DrawingSchema(
            code=drawing.code,
            post=PostSchema(code=post.code),
            author=UserSchema(
                code=author.code,
                email=author.email,
                nickname=author.nickname,
                profile_image_url=author.profile_image_url,
            ),
            content=drawing.content,
            image_urls=[image.url for image in images],
            created_at=drawing.created_at,
            updated_at=drawing.updated_at,
        )
        results.append(result)
    return DrawingListSchema(
        count=len(drawings),
        items=results,
    )


def get_drawing(session: Session, code: str) -> DrawingSchema:
    drawing = session.execute(
        select(Drawing).where(
            Drawing.code == code,
            Drawing.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if drawing is None:
        raise HTTPException(status_code=404, detail="Drawing not found")
    post = session.execute(
        select(Post).where(
            Post.id == drawing.post_id,
            Post.deleted_at.is_(None),
        )
    ).scalar_one()
    author = session.execute(
        select(User).where(
            User.id == drawing.author_id,
            User.deleted_at.is_(None),
        )
    ).scalar_one()
    images = (
        session.execute(
            select(Image).where(
                Image.drawing_id == drawing.id,
                Image.deleted_at.is_(None),
            )
        )
        .scalars()
        .all()
    )
    return DrawingSchema(
        code=drawing.code,
        post=PostSchema(code=post.code),
        author=UserSchema(
            code=author.code,
            email=author.email,
            nickname=author.nickname,
            profile_image_url=author.profile_image_url,
        ),
        content=drawing.content,
        image_urls=[image.url for image in images],
        created_at=drawing.created_at,
        updated_at=drawing.updated_at,
    )


def update_drawing(
    *,
    session: Session,
    code: str,
    schema: UpdateDrawingSchema,
    user: User,
) -> DrawingSchema:
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
    post = session.execute(
        select(Post).where(
            Post.id == drawing.post_id,
            Post.deleted_at.is_(None),
        )
    ).scalar_one()
    author = session.execute(
        select(User).where(
            User.id == drawing.author_id,
            User.deleted_at.is_(None),
        )
    ).scalar_one()
    images = (
        session.execute(
            select(Image).where(
                Image.drawing_id == drawing.id,
                Image.deleted_at.is_(None),
            )
        )
        .scalars()
        .all()
    )

    # drawing 수정
    drawing.content = schema.content
    session.add(drawing)

    # 기존 drawing images 전부 삭제
    for image in images:
        image.deleted_at = datetime.now(UTC)
        session.add(image)

    # 새로운 drawing images 생성
    images = []
    for image_url in schema.image_urls:
        image = Image(drawing_id=drawing.id, url=image_url)
        images.append(image)
    session.add_all(images)
    session.commit()

    return DrawingSchema(
        code=drawing.code,
        post=PostSchema(code=post.code),
        author=UserSchema(
            code=author.code,
            email=author.email,
            nickname=author.nickname,
            profile_image_url=author.profile_image_url,
        ),
        content=drawing.content,
        image_urls=[image.url for image in images],
        created_at=drawing.created_at,
        updated_at=drawing.updated_at,
    )


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
