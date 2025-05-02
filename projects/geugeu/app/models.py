from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, Identity, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.db import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger(), Identity(), primary_key=True)
    code: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    nickname: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    is_admin: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
    profile_image_url: Mapped[str] = mapped_column(
        String(2083),
        nullable=False,
        default="",
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


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(BigInteger(), Identity(), primary_key=True)
    code: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    author_id: Mapped[int] = mapped_column(BigInteger(), nullable=False)
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


class Drawing(Base):
    __tablename__ = "drawing"

    id: Mapped[int] = mapped_column(BigInteger(), Identity(), primary_key=True)
    code: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    post_id: Mapped[int] = mapped_column(BigInteger(), nullable=False)
    author_id: Mapped[int] = mapped_column(BigInteger(), nullable=False)
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


class Image(Base):
    __tablename__ = "image"

    id: Mapped[int] = mapped_column(BigInteger(), Identity(), primary_key=True)
    code: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    post_id: Mapped[int | None] = mapped_column(BigInteger(), nullable=True)
    drawing_id: Mapped[int | None] = mapped_column(BigInteger(), nullable=True)
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


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(BigInteger(), Identity(), primary_key=True)
    code: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    author_id: Mapped[int] = mapped_column(BigInteger(), nullable=False)
    post_id: Mapped[int | None] = mapped_column(BigInteger(), nullable=True)
    drawing_id: Mapped[int | None] = mapped_column(BigInteger(), nullable=True)
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
