from datetime import datetime

from pydantic import BaseModel, EmailStr


class SignupSchema(BaseModel):
    email: EmailStr
    password: str
    nickname: str | None = None


class UserSchema(BaseModel):
    code: str
    email: EmailStr
    nickname: str | None = None
    profile_image_url: str | None = None
    created_at: datetime
    updated_at: datetime


class UserUpdateSchema(BaseModel):
    nickname: str | None = None


class TokenPayload(BaseModel):
    sub: str | None = None
