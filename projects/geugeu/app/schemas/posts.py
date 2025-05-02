from datetime import datetime

from pydantic import BaseModel, EmailStr


class CreatePostSchema(BaseModel):
    title: str
    content: str
    image_urls: list[str] = []


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


class PostListSchema(BaseModel):
    count: int
    items: list[PostSchema]


class UpdatePostSchema(BaseModel):
    title: str
    content: str = ""
    image_urls: list[str] = []
