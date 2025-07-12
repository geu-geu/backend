from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.models import Interest


class UserSchema(BaseModel):
    code: str
    email: EmailStr
    nickname: str = ""
    profile_image_url: str = ""


class PostSchema(BaseModel):
    code: str
    title: str


class InterestSchema(BaseModel):
    code: str
    user: UserSchema
    post: PostSchema
    created_at: datetime

    @classmethod
    def from_model(cls, interest: Interest):
        return cls(
            code=interest.code,
            user=UserSchema(
                code=interest.user.code,
                email=interest.user.email,
                nickname=interest.user.nickname,
                profile_image_url=interest.user.profile_image_url,
            ),
            post=PostSchema(
                code=interest.post.code,
                title=interest.post.title,
            ),
            created_at=interest.created_at,
        )


class CreateInterestSchema(BaseModel):
    post_code: str


class InterestResponseSchema(BaseModel):
    success: bool
    message: str
    is_interested: bool


class InterestListSchema(BaseModel):
    items: list[InterestSchema]
    count: int
    is_interested: bool | None = None
