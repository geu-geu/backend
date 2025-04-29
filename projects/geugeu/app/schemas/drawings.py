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
    nickname: str | None = None
    profile_image_url: str | None = None


class DrawingSchema(BaseModel):
    code: str
    post: PostSchema
    author: UserSchema
    content: str
    image_urls: list[str]
    created_at: datetime
    updated_at: datetime
