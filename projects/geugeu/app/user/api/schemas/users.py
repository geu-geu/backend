from pydantic import BaseModel


class SignupBody(BaseModel):
    email: str
    password: str
    name: str | None = None
