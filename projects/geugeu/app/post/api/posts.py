from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from ulid import ULID

from app.auth.dependencies import CurrentActiveUserDep
from app.database import SessionDep
from app.post.application.post_service import PostService
from app.post.dependencies import post_service
from app.post.domain.post import Post
from app.post.domain.post_comment import PostComment

router = APIRouter(prefix="/posts", tags=["posts"])


class CreatePostBody(BaseModel):
    title: str
    content: str
    image_urls: list[str] = Field(default_factory=list)


class UpdatePostBody(BaseModel):
    title: str
    content: str
    image_urls: list[str] = Field(default_factory=list)


class PostResponse(BaseModel):
    id: str
    title: str
    content: str
    images: list[str]
    created_at: datetime
    updated_at: datetime


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    body: CreatePostBody,
    post_service: Annotated[PostService, Depends(post_service)],
    session: SessionDep,
    user: CurrentActiveUserDep,
) -> PostResponse:
    post = Post(
        id=str(ULID()),
        author_id=user.id,
        title=body.title,
        content=body.content,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post, images = post_service.create_post(
        session, post=post, image_urls=body.image_urls
    )
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        images=[image.image_url for image in images],
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: str,
    post_service: Annotated[PostService, Depends(post_service)],
    session: SessionDep,
    user: CurrentActiveUserDep,
) -> PostResponse:
    post, images = post_service.get_post(session, post_id=post_id)
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        images=[image.image_url for image in images],
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str,
    body: UpdatePostBody,
    post_service: Annotated[PostService, Depends(post_service)],
    session: SessionDep,
    user: CurrentActiveUserDep,
) -> PostResponse:
    post, images = post_service.update_post(
        session,
        post_id=post_id,
        title=body.title,
        content=body.content,
        image_urls=body.image_urls,
    )
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        images=[image.image_url for image in images],
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: str,
    post_service: Annotated[PostService, Depends(post_service)],
    session: SessionDep,
    user: CurrentActiveUserDep,
) -> None:
    post_service.delete_post(session, post_id=post_id)


class CreatePostCommentBody(BaseModel):
    content: str


class PostCommentResponse(BaseModel):
    id: str
    author_id: str
    post_id: str
    content: str
    created_at: datetime
    updated_at: datetime


@router.post(
    "/{post_id}/comments",
    response_model=PostCommentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_post_comment(
    post_id: str,
    body: CreatePostCommentBody,
    post_service: Annotated[PostService, Depends(post_service)],
    session: SessionDep,
    user: CurrentActiveUserDep,
) -> PostCommentResponse:
    post_comment = PostComment(
        id=str(ULID()),
        author_id=user.id,
        post_id=post_id,
        content=body.content,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_comment = post_service.create_post_comment(session, post_comment=post_comment)
    return PostCommentResponse(
        id=post_comment.id,
        author_id=post_comment.author_id,
        post_id=post_comment.post_id,
        content=post_comment.content,
        created_at=post_comment.created_at,
        updated_at=post_comment.updated_at,
    )
