from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class GoogleToken(BaseModel):
    access_token: str
    expires_in: int
    scope: str
    token_type: str
    id_token: str


class GoogleUser(BaseModel):
    id: str
    email: str
    verified_email: bool
    name: str = ""
    given_name: str = ""
    family_name: str = ""
    picture: str = ""
