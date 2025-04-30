from datetime import datetime

from sqlmodel import Session, not_, select

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
            nickname=user.nickname,
            profile_image_url=user.profile_image_url,
        ),
        title=post.title,
        content=post.content,
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


def get_posts(session: Session) -> PostListSchema:
    posts = session.exec(select(Post).order_by(Post.id.desc())).all()
    results = []
    for post in posts:
        author = session.exec(select(User).where(User.id == post.author_id)).one()
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
    post = session.exec(select(Post).where(Post.code == code)).one()
    author = session.exec(select(User).where(User.id == post.author_id)).one()
    images = session.exec(
        select(PostImage).where(
            PostImage.post_id == post.id,
            not_(PostImage.is_deleted),
        )
    ).all()
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
    post = session.exec(select(Post).where(Post.code == code)).one()
    images = session.exec(select(PostImage).where(PostImage.post_id == post.id)).all()
    author = session.exec(select(User).where(User.id == post.author_id)).one()

    # post 수정
    post.title = schema.title
    post.content = schema.content
    post.updated_at = datetime.now()
    session.add(post)

    # 기존 post images 삭제
    for image in images:
        image.is_deleted = True
        image.updated_at = datetime.now()
        session.add(image)

    # 새로운 post images 생성
    post_images = []
    for image_url in schema.image_urls:
        post_image = PostImage(
            code=generate_code(),
            post_id=post.id,
            image_url=image_url,
            is_deleted=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
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
    post = session.exec(select(Post).where(Post.code == code)).one()
    post.is_deleted = True
    session.commit()
