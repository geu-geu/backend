from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from ulid import ULID

from app.auth.dependencies import CurrentActiveUserDep
from app.post.application.post_service import PostService
from app.post.dependencies import post_service
from app.post.domain.post import Post

router = APIRouter(prefix="/posts", tags=["posts"])


class CreatePostBody(BaseModel):
    title: str
    content: str
    image_urls: list[str] = Field(default_factory=list)


class CreatePostResponse(BaseModel):
    id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    images: list[str]


@router.post("/")
async def create_post(
    body: CreatePostBody,
    post_service: Annotated[PostService, Depends(post_service)],
    user: CurrentActiveUserDep,
):
    post = Post(
        id=str(ULID()),
        author_id=user.id,
        title=body.title,
        content=body.content,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post, images = post_service.create_post(post=post, image_urls=body.image_urls)
    return CreatePostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        images=[image.image_url for image in images],
        created_at=post.created_at,
        updated_at=post.updated_at,
    )
