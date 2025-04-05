from datetime import datetime

from pydantic import BaseModel, Field


class CreatePostBody(BaseModel):
    title: str
    content: str
    image_urls: list[str] = Field(default_factory=list)


class UpdatePostBody(BaseModel):
    title: str
    content: str
    image_urls: list[str] = Field(default_factory=list)


class PostResponse(BaseModel):
    id: str
    title: str
    content: str
    images: list[str]
    created_at: datetime
    updated_at: datetime


class UpdatePostCommentBody(BaseModel):
    content: str


class CreatePostCommentBody(BaseModel):
    content: str


class PostCommentResponse(BaseModel):
    id: str
    author_id: str
    post_id: str
    content: str
    created_at: datetime
    updated_at: datetime
