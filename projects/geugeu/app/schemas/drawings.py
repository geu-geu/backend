from datetime import datetime

from pydantic import BaseModel, EmailStr


class CreateDrawingSchema(BaseModel):
    post_code: str
    content: str
    image_urls: list[str]


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


class DrawingListSchema(BaseModel):
    count: int
    items: list[DrawingSchema]


class UpdateDrawingSchema(BaseModel):
    content: str
    image_urls: list[str]
