from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.models import Drawing


class PostSchema(BaseModel):
    code: str


class UserSchema(BaseModel):
    code: str
    email: EmailStr
    nickname: str = ""
    profile_image_url: str = ""


class ImageSchema(BaseModel):
    url: str
    created_at: datetime
    updated_at: datetime


class DrawingSchema(BaseModel):
    code: str
    post: PostSchema
    author: UserSchema
    content: str
    images: list[ImageSchema]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_model(cls, drawing: Drawing):
        return cls(
            code=drawing.code,
            post=PostSchema(code=drawing.post.code),
            author=UserSchema(
                code=drawing.author.code,
                email=drawing.author.email,
                nickname=drawing.author.nickname,
                profile_image_url=drawing.author.profile_image_url,
            ),
            content=drawing.content,
            images=[
                ImageSchema(
                    url=image.url,
                    created_at=image.created_at,
                    updated_at=image.updated_at,
                )
                for image in drawing.images
            ],
            created_at=drawing.created_at,
            updated_at=drawing.updated_at,
        )


class DrawingListSchema(BaseModel):
    count: int
    items: list[DrawingSchema]
