from datetime import datetime

from pydantic import BaseModel

from app.models import Comment


class CreateCommentSchema(BaseModel):
    content: str
    parent_code: str | None = None


class UserSchema(BaseModel):
    code: str
    email: str
    nickname: str
    profile_image_url: str


class CommentSchema(BaseModel):
    code: str
    author: UserSchema
    content: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_model(cls, comment: Comment):
        return cls(
            code=comment.code,
            author=UserSchema(
                code=comment.author.code,
                email=comment.author.email,
                nickname=comment.author.nickname,
                profile_image_url=comment.author.profile_image_url,
            ),
            content=comment.content,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )


class CommentListSchema(BaseModel):
    count: int
    items: list[CommentSchema]


class UpdateCommentSchema(BaseModel):
    content: str
