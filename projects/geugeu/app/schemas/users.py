from datetime import datetime

from pydantic import BaseModel, EmailStr


class SignupSchema(BaseModel):
    email: EmailStr
    password: str
    nickname: str = ""


class UserSchema(BaseModel):
    code: str
    email: EmailStr
    nickname: str = ""
    profile_image_url: str = ""
    created_at: datetime
    updated_at: datetime


class UserUpdateSchema(BaseModel):
    nickname: str


class TokenPayload(BaseModel):
    sub: str | None = None
