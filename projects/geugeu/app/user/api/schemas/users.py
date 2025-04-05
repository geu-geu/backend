from pydantic import BaseModel, EmailStr


class SignupBody(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None
