from datetime import datetime

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: str = Field(max_length=255, primary_key=True)
    email: str = Field(max_length=255, unique=True, nullable=False)
    name: str | None = Field(max_length=255, nullable=True)
    password: str = Field(max_length=255, nullable=False)
    is_admin: bool = Field(default=False, nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    is_verified: bool = Field(default=False, nullable=False)
    profile_image_url: str | None = Field(max_length=2000, nullable=True)
    created_at: datetime = Field(nullable=False)
    updated_at: datetime = Field(nullable=False)


class Post(SQLModel, table=True):
    id: str = Field(max_length=255, primary_key=True)
    author_id: str = Field(max_length=255, nullable=False)
    title: str = Field(max_length=255, nullable=False)
    content: str = Field(nullable=False)
    created_at: datetime = Field(nullable=False)
    updated_at: datetime = Field(nullable=False)


class PostImage(SQLModel, table=True):
    id: str = Field(max_length=255, primary_key=True)
    post_id: str = Field(max_length=255, nullable=False)
    image_url: str = Field(max_length=2000, nullable=False)


class Comment(SQLModel, table=True):
    id: str = Field(max_length=255, primary_key=True)
    author_id: str = Field(max_length=255, nullable=False)
    post_id: str = Field(max_length=255, nullable=False)
    content: str = Field(nullable=False)
    created_at: datetime = Field(nullable=False)
    updated_at: datetime = Field(nullable=False)


class Like(SQLModel, table=True):
    id: str = Field(max_length=255, primary_key=True)
    author_id: str = Field(max_length=255, nullable=False)
    post_id: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(nullable=False)
    updated_at: datetime = Field(nullable=False)
