from datetime import datetime

from pydantic import BaseModel


class CreateCommentSchema(BaseModel):
    content: str


class UserSchema(BaseModel):
    code: str
    email: str
    nickname: str
    profile_image_url: str


class CommentSchema(BaseModel):
    code: str
    author: UserSchema
    content: str
    created_at: datetime
    updated_at: datetime


class CommentListSchema(BaseModel):
    count: int
    items: list[CommentSchema]


class UpdateCommentSchema(BaseModel):
    content: str
