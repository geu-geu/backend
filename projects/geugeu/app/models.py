from datetime import datetime

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: str = Field(max_length=255, primary_key=True)
    email: str = Field(max_length=255, unique=True, nullable=False)
    name: str | None = Field(max_length=255, nullable=True)
    password: str = Field(max_length=255, nullable=False)
    is_admin: bool = Field(default=False, nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(nullable=False)
    updated_at: datetime = Field(nullable=False)
