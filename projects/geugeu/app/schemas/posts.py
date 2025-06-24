from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.models import Post


class UserSchema(BaseModel):
    code: str
    email: EmailStr
    nickname: str = ""
    profile_image_url: str = ""


class ImageSchema(BaseModel):
    url: str
    created_at: datetime
    updated_at: datetime


class PostSchema(BaseModel):
    code: str
    author: UserSchema
    title: str
    content: str
    images: list[ImageSchema]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_model(cls, post: Post):
        return cls(
            code=post.code,
            author=UserSchema(
                code=post.author.code,
                email=post.author.email,
                nickname=post.author.nickname,
                profile_image_url=post.author.profile_image_url,
            ),
            title=post.title,
            content=post.content,
            images=[
                ImageSchema(
                    url=image.url,
                    created_at=image.created_at,
                    updated_at=image.updated_at,
                )
                for image in post.images
            ],
            created_at=post.created_at,
            updated_at=post.updated_at,
        )


class PostListSchema(BaseModel):
    count: int
    items: list[PostSchema]


class PostListFilter(BaseModel):
    author_code: str | None = None

    page: int = 1
    page_size: int = 10
