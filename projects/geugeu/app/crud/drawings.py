from datetime import UTC, datetime

from sqlmodel import Session, delete, select

from app.models import Drawing, DrawingImage, Post, User
from app.schemas.drawings import (
    CreateDrawingSchema,
    DrawingListSchema,
    DrawingSchema,
    PostSchema,
    UpdateDrawingSchema,
    UserSchema,
)
from app.utils import generate_code


def create_drawing(
    session: Session, user: User, schema: CreateDrawingSchema
) -> DrawingSchema:
    post = session.exec(select(Post).where(Post.code == schema.post_code)).one()
    drawing = Drawing(
        code=generate_code(),
        post_id=post.id,
        author_id=user.id,
        content=schema.content,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    session.add(drawing)
    session.commit()
    drawing_images = []
    for image_url in schema.image_urls:
        drawing_image = DrawingImage(
            code=generate_code(),
            drawing_id=drawing.id,
            image_url=image_url,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        drawing_images.append(drawing_image)
    session.add_all(drawing_images)
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
        image_urls=[drawing_image.image_url for drawing_image in drawing_images],
        created_at=drawing.created_at,
        updated_at=drawing.updated_at,
    )


def get_drawings(session: Session) -> DrawingListSchema:
    drawings = session.exec(select(Drawing).order_by(Drawing.id.desc())).all()
    results = []
    for drawing in drawings:
        post = session.exec(select(Post).where(Post.id == drawing.post_id)).one()
        author = session.exec(select(User).where(User.id == drawing.author_id)).one()
        images = session.exec(
            select(DrawingImage).where(DrawingImage.drawing_id == drawing.id)
        ).all()
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
            image_urls=[drawing_image.image_url for drawing_image in images],
            created_at=drawing.created_at,
            updated_at=drawing.updated_at,
        )
        results.append(result)
    return DrawingListSchema(
        count=len(drawings),
        items=results,
    )


def get_drawing(session: Session, code: str) -> DrawingSchema:
    drawing = session.exec(select(Drawing).where(Drawing.code == code)).one()
    post = session.exec(select(Post).where(Post.id == drawing.post_id)).one()
    author = session.exec(select(User).where(User.id == drawing.author_id)).one()
    images = session.exec(
        select(DrawingImage).where(DrawingImage.drawing_id == drawing.id)
    ).all()
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
        image_urls=[drawing_image.image_url for drawing_image in images],
        created_at=drawing.created_at,
        updated_at=drawing.updated_at,
    )


def update_drawing(
    session: Session, code: str, schema: UpdateDrawingSchema
) -> DrawingSchema:
    drawing = session.exec(select(Drawing).where(Drawing.code == code)).one()
    post = session.exec(select(Post).where(Post.id == drawing.post_id)).one()
    author = session.exec(select(User).where(User.id == drawing.author_id)).one()
    images = session.exec(
        select(DrawingImage).where(DrawingImage.drawing_id == drawing.id)
    ).all()

    # drawing 수정
    drawing.content = schema.content
    drawing.updated_at = datetime.now(UTC)
    session.add(drawing)

    # drawing images 전부 삭제 후 재생성
    for image in images:
        image.is_deleted = True
        session.add(image)

    drawing_images = []
    for image_url in schema.image_urls:
        drawing_image = DrawingImage(
            code=generate_code(),
            drawing_id=drawing.id,
            image_url=image_url,
            is_deleted=False,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        drawing_images.append(drawing_image)
    session.add_all(drawing_images)
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
        image_urls=[drawing_image.image_url for drawing_image in drawing_images],
        created_at=drawing.created_at,
        updated_at=drawing.updated_at,
    )
