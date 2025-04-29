from datetime import UTC, datetime

from sqlmodel import Session, select

from app.models import Drawing, DrawingImage, Post, User
from app.schemas.drawings import (
    CreateDrawingSchema,
    DrawingSchema,
    PostSchema,
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
