from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Post, PostImage, User
from app.schemas.posts import (
    CreatePostSchema,
    PostListSchema,
    PostSchema,
    UpdatePostSchema,
    UserSchema,
)
from app.utils import generate_code


def create_post(session: Session, user: User, schema: CreatePostSchema) -> PostSchema:
    post = Post(
        code=generate_code(),
        author_id=user.id,
        title=schema.title,
        content=schema.content,
    )
    session.add(post)
    session.flush()

    post_images = []
    for image_url in schema.image_urls:
        post_image = PostImage(
            code=generate_code(),
            post_id=post.id,
            image_url=image_url,
        )
        post_images.append(post_image)
    session.add_all(post_images)
    session.commit()

    return PostSchema(
        code=post.code,
        author=UserSchema(
            code=user.code,
            email=user.email,
            nickname=user.nickname,
            profile_image_url=user.profile_image_url,
        ),
        title=post.title,
        content=post.content,
        image_urls=[post_image.image_url for post_image in post_images],
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


def get_posts(session: Session) -> PostListSchema:
    posts = (
        session.execute(
            select(Post).where(Post.deleted_at.is_(None)).order_by(Post.id.desc())
        )
        .scalars()
        .all()
    )
    results = []
    for post in posts:
        author = session.execute(
            select(User).where(
                User.id == post.author_id,
                User.deleted_at.is_(None),
            )
        ).scalar_one()
        result = PostSchema(
            code=post.code,
            author=UserSchema(
                code=author.code,
                email=author.email,
                nickname=author.nickname,
                profile_image_url=author.profile_image_url,
            ),
            title=post.title,
            content=post.content,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )
        results.append(result)
    return PostListSchema(
        count=len(posts),
        items=results,
    )


def get_post(session: Session, code: str) -> PostSchema:
    post = session.execute(
        select(Post).where(
            Post.code == code,
            Post.deleted_at.is_(None),
        )
    ).scalar_one()
    author = session.execute(
        select(User).where(
            User.id == post.author_id,
            User.deleted_at.is_(None),
        )
    ).scalar_one()
    images = (
        session.execute(
            select(PostImage).where(
                PostImage.post_id == post.id,
                PostImage.deleted_at.is_(None),
            )
        )
        .scalars()
        .all()
    )
    return PostSchema(
        code=post.code,
        author=UserSchema(
            code=author.code,
            email=author.email,
            nickname=author.nickname,
            profile_image_url=author.profile_image_url,
        ),
        title=post.title,
        content=post.content,
        image_urls=[image.image_url for image in images],
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


def update_post(session: Session, code: str, schema: UpdatePostSchema) -> PostSchema:
    post = session.execute(
        select(Post).where(
            Post.code == code,
            Post.deleted_at.is_(None),
        )
    ).scalar_one()
    author = session.execute(
        select(User).where(
            User.id == post.author_id,
            User.deleted_at.is_(None),
        )
    ).scalar_one()
    images = (
        session.execute(
            select(PostImage).where(
                PostImage.post_id == post.id,
                PostImage.deleted_at.is_(None),
            )
        )
        .scalars()
        .all()
    )

    # post 수정
    post.title = schema.title
    post.content = schema.content
    session.add(post)

    # 기존 post images 전부 삭제
    for image in images:
        image.deleted_at = datetime.now(UTC)
        session.add(image)

    # 새로운 post images 생성
    post_images = []
    for image_url in schema.image_urls:
        post_image = PostImage(
            code=generate_code(),
            post_id=post.id,
            image_url=image_url,
        )
        post_images.append(post_image)
    session.add_all(post_images)
    session.commit()

    return PostSchema(
        code=post.code,
        author=UserSchema(
            code=author.code,
            email=author.email,
            nickname=author.nickname,
            profile_image_url=author.profile_image_url,
        ),
        title=post.title,
        content=post.content,
        image_urls=[post_image.image_url for post_image in post_images],
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


def delete_post(session: Session, code: str) -> None:
    post = session.execute(
        select(Post).where(
            Post.code == code,
            Post.deleted_at.is_(None),
        )
    ).scalar_one()
    post.deleted_at = datetime.now(UTC)
    session.commit()
