import re
from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator


class SignupSchema(BaseModel):
    email: EmailStr
    password: str
    nickname: str = ""

    @field_validator("password")
    def validate_password(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]", password):
            raise ValueError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError("Password must contain at least one special character.")
        return password


class UserSchema(BaseModel):
    code: str
    email: EmailStr
    nickname: str = ""
    profile_image_url: str = ""
    created_at: datetime
    updated_at: datetime


class UserUpdateSchema(BaseModel):
    nickname: str
