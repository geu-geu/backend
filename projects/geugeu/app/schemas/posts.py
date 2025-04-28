from datetime import datetime

from pydantic import BaseModel, EmailStr


class CreatePostSchema(BaseModel):
    title: str
    content: str


class UserSchema(BaseModel):
    code: str
    email: EmailStr
    name: str | None = None
    profile_image_url: str | None = None


class PostSchema(BaseModel):
    code: str
    author: UserSchema
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
