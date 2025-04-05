from datetime import datetime

from pydantic import BaseModel, Field


class CreateDrawingBody(BaseModel):
    post_id: str
    content: str = ""  # 초기에는 빈 내용일 수 있음
    image_urls: list[str] = Field(default_factory=list)


class UpdateDrawingBody(BaseModel):
    content: str
    image_urls: list[str] = Field(default_factory=list)


class CompleteDrawingBody(BaseModel):
    content: str
    image_urls: list[str] = Field(default_factory=list)


class DrawingResponse(BaseModel):
    id: str
    post_id: str
    content: str
    images: list[str]
    status: str
    created_at: datetime
    updated_at: datetime


class UpdateDrawingCommentBody(BaseModel):
    content: str


class CreateDrawingCommentBody(BaseModel):
    content: str


class DrawingCommentResponse(BaseModel):
    id: str
    author_id: str
    drawing_id: str
    content: str
    created_at: datetime
    updated_at: datetime
