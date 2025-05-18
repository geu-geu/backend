from datetime import datetime
from enum import StrEnum
from typing import List, Optional

from nanoid import generate
from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Identity,
    String,
    Text,
    and_,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.db import Base


def generate_code() -> str:
    return generate()


class User(Base):
    __tablename__ = "user"

    class AuthProvider(StrEnum):
        LOCAL = "LOCAL"
        GOOGLE = "GOOGLE"
        APPLE = "APPLE"

    id: Mapped[int] = mapped_column(BigInteger(), Identity(), primary_key=True)
    code: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        default=generate_code,
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    nickname: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    is_admin: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
    profile_image_url: Mapped[str] = mapped_column(
        String(2083),
        nullable=False,
        default="",
    )
    auth_provider: Mapped[AuthProvider] = mapped_column(
        Enum(AuthProvider, native_enum=False, length=30),
        nullable=False,
        server_default=AuthProvider.LOCAL,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    posts: Mapped[List["Post"]] = relationship(
        "Post",
        primaryjoin=lambda: and_(
            Post.author_id == User.id,
            Post.deleted_at.is_(None),
        ),
        back_populates="author",
    )
    drawings: Mapped[List["Drawing"]] = relationship(
        "Drawing",
        primaryjoin=lambda: and_(
            Drawing.author_id == User.id,
            Drawing.deleted_at.is_(None),
        ),
        back_populates="author",
    )
    comments: Mapped[List["Comment"]] = relationship(
        "Comment",
        primaryjoin=lambda: and_(
            Comment.author_id == User.id,
            Comment.deleted_at.is_(None),
        ),
        back_populates="author",
    )


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(BigInteger(), Identity(), primary_key=True)
    code: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        default=generate_code,
    )
    author_id: Mapped[int] = mapped_column(
        BigInteger(),
        ForeignKey("user.id"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    author: Mapped["User"] = relationship(back_populates="posts")
    drawings: Mapped[List["Drawing"]] = relationship(
        "Drawing",
        primaryjoin=lambda: and_(
            Drawing.post_id == Post.id,
            Drawing.deleted_at.is_(None),
        ),
        back_populates="post",
    )
    images: Mapped[List["Image"]] = relationship(
        "Image",
        primaryjoin=lambda: and_(
            Image.post_id == Post.id,
            Image.deleted_at.is_(None),
        ),
        back_populates="post",
    )
    comments: Mapped[List["Comment"]] = relationship(
        "Comment",
        primaryjoin=lambda: and_(
            Comment.post_id == Post.id,
            Comment.deleted_at.is_(None),
        ),
        back_populates="post",
    )


class Drawing(Base):
    __tablename__ = "drawing"

    id: Mapped[int] = mapped_column(BigInteger(), Identity(), primary_key=True)
    code: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        default=generate_code,
    )
    post_id: Mapped[int] = mapped_column(
        BigInteger(),
        ForeignKey("post.id"),
        nullable=False,
    )
    author_id: Mapped[int] = mapped_column(
        BigInteger(),
        ForeignKey("user.id"),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    post: Mapped["Post"] = relationship(back_populates="drawings")
    author: Mapped["User"] = relationship(back_populates="drawings")
    images: Mapped[List["Image"]] = relationship(
        "Image",
        primaryjoin=lambda: and_(
            Drawing.id == Image.drawing_id, Image.deleted_at.is_(None)
        ),
        back_populates="drawing",
    )
    comments: Mapped[List["Comment"]] = relationship(
        "Comment",
        primaryjoin=lambda: and_(
            Drawing.id == Comment.drawing_id, Comment.deleted_at.is_(None)
        ),
        back_populates="drawing",
    )


class Image(Base):
    __tablename__ = "image"

    id: Mapped[int] = mapped_column(BigInteger(), Identity(), primary_key=True)
    code: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        default=generate_code,
    )
    post_id: Mapped[int | None] = mapped_column(
        BigInteger(),
        ForeignKey("post.id"),
        nullable=True,
    )
    drawing_id: Mapped[int | None] = mapped_column(
        BigInteger(),
        ForeignKey("drawing.id"),
        nullable=True,
    )
    url: Mapped[str] = mapped_column(String(2083), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    post: Mapped[Optional["Post"]] = relationship(back_populates="images")
    drawing: Mapped[Optional["Drawing"]] = relationship(back_populates="images")


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(BigInteger(), Identity(), primary_key=True)
    code: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        default=generate_code,
    )
    author_id: Mapped[int] = mapped_column(
        BigInteger(),
        ForeignKey("user.id"),
        nullable=False,
    )
    post_id: Mapped[int | None] = mapped_column(
        BigInteger(),
        ForeignKey("post.id"),
        nullable=True,
    )
    drawing_id: Mapped[int | None] = mapped_column(
        BigInteger(),
        ForeignKey("drawing.id"),
        nullable=True,
    )
    parent_id: Mapped[int | None] = mapped_column(
        BigInteger(),
        ForeignKey("comment.id"),
        nullable=True,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationships
    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped[Optional["Post"]] = relationship(back_populates="comments")
    drawing: Mapped[Optional["Drawing"]] = relationship(back_populates="comments")
    parent: Mapped[Optional["Comment"]] = relationship(
        back_populates="replies", remote_side=[id]
    )
    replies: Mapped[List["Comment"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan"
    )
