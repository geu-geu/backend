from typing import Literal

from pydantic import BaseModel, EmailStr


class SignupBody(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None


class UpdateProfileImageBody(BaseModel):
    profile_image_url: str


class CreateProfileImageUploadURLBody(BaseModel):
    file_extension: Literal[".png", ".jpeg", ".jpg", ".webp"]
