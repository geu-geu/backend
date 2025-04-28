from datetime import datetime

from sqlmodel import Session, select

from app.models import Post, User
from app.schemas.posts import CreatePostSchema, PostSchema, UserSchema
from app.utils import generate_code


def create_post(session: Session, user: User, schema: CreatePostSchema) -> PostSchema:
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


def get_posts(session: Session) -> list[PostSchema]:
    posts = session.exec(select(Post).order_by(Post.id.desc())).all()
    results = []
    for post in posts:
        author = session.exec(select(User).where(User.id == post.author_id)).one()
        result = PostSchema(
            code=post.code,
            author=UserSchema(
                code=author.code,
                email=author.email,
                name=author.name,
                profile_image_url=author.profile_image_url,
            ),
            title=post.title,
            content=post.content,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )
        results.append(result)
    return results
