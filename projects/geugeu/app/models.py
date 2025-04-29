from datetime import datetime

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(max_length=255, unique=True, nullable=False)
    email: str = Field(max_length=255, unique=True, nullable=False)
    nickname: str | None = Field(max_length=255, nullable=True)
    password: str = Field(max_length=255, nullable=False)
    is_admin: bool = Field(default=False, nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    profile_image_url: str | None = Field(max_length=2000, nullable=True)
    created_at: datetime = Field(nullable=False)
    updated_at: datetime = Field(nullable=False)


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(max_length=255, unique=True, nullable=False)
    author_id: int = Field(nullable=False)
    title: str = Field(max_length=255, nullable=False)
    content: str = Field(nullable=False)
    is_deleted: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(nullable=False)
    updated_at: datetime = Field(nullable=False)


class PostImage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(max_length=255, unique=True, nullable=False)
    post_id: int = Field(nullable=False)
    image_url: str = Field(max_length=2000, nullable=False)


class PostComment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(max_length=255, unique=True, nullable=False)
    author_id: int = Field(nullable=False)
    post_id: int = Field(nullable=False)
    content: str = Field(nullable=False)
    created_at: datetime = Field(nullable=False)
    updated_at: datetime = Field(nullable=False)


class Drawing(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(max_length=255, unique=True, nullable=False)
    post_id: int = Field(nullable=False)
    author_id: int = Field(nullable=False)
    content: str = Field(nullable=False)
    created_at: datetime = Field(nullable=False)
    updated_at: datetime = Field(nullable=False)


class DrawingImage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(max_length=255, unique=True, nullable=False)
    drawing_id: int = Field(nullable=False)
    image_url: str = Field(max_length=2000, nullable=False)


class DrawingComment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(max_length=255, unique=True, nullable=False)
    author_id: int = Field(nullable=False)
    drawing_id: int = Field(nullable=False)
    content: str = Field(nullable=False)
    created_at: datetime = Field(nullable=False)
    updated_at: datetime = Field(nullable=False)
