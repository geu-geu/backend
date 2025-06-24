from datetime import UTC, datetime

from fastapi import HTTPException, UploadFile
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload, selectinload, with_loader_criteria

from app.models import Image, Post, User
from app.schemas.posts import PostListFilter, PostListSchema, PostSchema
from app.utils import upload_file


def create_post(
    db: Session,
    user: User,
    title: str,
    content: str,
    files: list[UploadFile],
) -> PostSchema:
    with db.begin_nested():
        post = Post(author_id=user.id, title=title, content=content)
        db.add(post)
        db.flush()

        post_images = []
        for file in files:
            url = upload_file(file)
            post_image = Image(post_id=post.id, url=url)
            post_images.append(post_image)
        db.add_all(post_images)

    db.commit()
    return PostSchema.from_model(post)


def get_posts(db: Session, filters: PostListFilter) -> PostListSchema:
    stmt = (
        select(Post)
        .options(
            joinedload(Post.author),
            selectinload(Post.images),
            with_loader_criteria(Image, Image.deleted_at.is_(None)),
        )
        .where(Post.deleted_at.is_(None))
        .order_by(Post.id.desc())
    )

    if filters.author_code:
        stmt = stmt.join(User, Post.author_id == User.id).where(
            User.code == filters.author_code
        )

    offset = (filters.page - 1) * filters.page_size
    count = db.execute(select(func.count()).select_from(stmt.subquery())).scalar_one()
    rows = db.execute(stmt.offset(offset).limit(filters.page_size)).scalars().all()
    return PostListSchema(
        count=count,
        items=[PostSchema.from_model(row) for row in rows],
    )


def get_post(db: Session, code: str) -> PostSchema:
    post = db.execute(
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
    db: Session,
    code: str,
    user: User,
    title: str,
    content: str,
    files: list[UploadFile],
) -> PostSchema:
    post = db.execute(
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

    with db.begin_nested():
        # post 수정
        post.title = title
        post.content = content
        db.add(post)

        # 기존 post images 전부 삭제
        for image in post.images:
            image.deleted_at = datetime.now(UTC)
            db.add(image)

        # 새로운 post images 생성
        images = []
        for file in files:
            url = upload_file(file)
            image = Image(post_id=post.id, url=url)
            images.append(image)
        db.add_all(images)

    db.commit()
    db.refresh(post)
    return PostSchema.from_model(post)


def delete_post(*, db: Session, code: str, user: User) -> None:
    post = db.execute(
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
    db.commit()
