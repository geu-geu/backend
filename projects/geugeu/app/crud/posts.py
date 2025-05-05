from datetime import UTC, datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload, with_loader_criteria

from app.models import Image, Post, User
from app.schemas.posts import (
    CreatePostSchema,
    PostListSchema,
    PostSchema,
    UpdatePostSchema,
)


def create_post(session: Session, user: User, payload: CreatePostSchema) -> PostSchema:
    post = Post(
        author_id=user.id,
        title=payload.title,
        content=payload.content,
    )
    session.add(post)
    session.flush()

    post_images = []
    for image_url in payload.image_urls:
        post_image = Image(post_id=post.id, url=image_url)
        post_images.append(post_image)
    session.add_all(post_images)
    session.commit()
    return PostSchema.from_model(post)


def get_posts(session: Session) -> PostListSchema:
    posts = (
        session.execute(
            select(Post)
            .options(
                joinedload(Post.author),
                selectinload(Post.images),
                with_loader_criteria(Image, Image.deleted_at.is_(None)),
            )
            .where(Post.deleted_at.is_(None))
            .order_by(Post.id.desc())
        )
        .scalars()
        .unique()
        .all()
    )
    return PostListSchema(
        count=len(posts),
        items=[PostSchema.from_model(post) for post in posts],
    )


def get_post(session: Session, code: str) -> PostSchema:
    post = session.execute(
        select(Post)
        .options(
            joinedload(Post.author),
            selectinload(Post.images),
            with_loader_criteria(Image, Image.deleted_at.is_(None)),
        )
        .where(
            Post.code == code,
            Post.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostSchema.from_model(post)


def update_post(
    *,
    session: Session,
    code: str,
    payload: UpdatePostSchema,
    user: User,
) -> PostSchema:
    post = session.execute(
        select(Post)
        .options(
            joinedload(Post.author),
            selectinload(Post.images),
            with_loader_criteria(Image, Image.deleted_at.is_(None)),
        )
        .where(
            Post.code == code,
            Post.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id == user.id or user.is_admin:
        pass
    else:
        raise HTTPException(status_code=403, detail="Forbidden")

    # post 수정
    post.title = payload.title
    post.content = payload.content
    session.add(post)

    # 기존 post images 전부 삭제
    for image in post.images:
        image.deleted_at = datetime.now(UTC)
        session.add(image)

    # 새로운 post images 생성
    images = []
    for image_url in payload.image_urls:
        image = Image(post_id=post.id, url=image_url)
        images.append(image)
    session.add_all(images)
    session.commit()
    session.refresh(post)
    return PostSchema.from_model(post)


def delete_post(*, session: Session, code: str, user: User) -> None:
    post = session.execute(
        select(Post).where(
            Post.code == code,
            Post.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id == user.id or user.is_admin:
        pass
    else:
        raise HTTPException(status_code=403, detail="Forbidden")
    post.deleted_at = datetime.now(UTC)
    session.commit()
