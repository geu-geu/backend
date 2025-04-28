from datetime import datetime

from sqlmodel import Session

from app.models import Post, User
from app.schemas.posts import CreatePostSchema, PostSchema, UserSchema
from app.utils import generate_code


def create_post(session: Session, user: User, schema: CreatePostSchema):
    post = Post(
        code=generate_code(),
        author_id=user.id,
        title=schema.title,
        content=schema.content,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    session.add(post)
    session.commit()
    session.refresh(post)
    return PostSchema(
        code=post.code,
        author=UserSchema(
            code=user.code,
            email=user.email,
            name=user.name,
            profile_image_url=user.profile_image_url,
        ),
        title=post.title,
        content=post.content,
        created_at=post.created_at,
        updated_at=post.updated_at,
    )
