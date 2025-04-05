from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status
from ulid import ULID

from app.auth.deps import CurrentUserDep
from app.database import SessionDep
from app.post.api.schemas.posts import (
    CreatePostBody,
    CreatePostCommentBody,
    PostCommentResponse,
    PostResponse,
    UpdatePostBody,
    UpdatePostCommentBody,
)
from app.post.deps import post_service
from app.post.domain.post import Post
from app.post.domain.post_comment import PostComment
from app.post.services.post_service import PostService

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    body: CreatePostBody,
    post_service: Annotated[PostService, Depends(post_service)],
    session: SessionDep,
    user: CurrentUserDep,
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
    user: CurrentUserDep,
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
    user: CurrentUserDep,
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
    user: CurrentUserDep,
) -> None:
    post_service.delete_post(session, post_id=post_id)


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
    user: CurrentUserDep,
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


@router.get("/{post_id}/comments", response_model=list[PostCommentResponse])
async def get_post_comments(
    post_id: str,
    post_service: Annotated[PostService, Depends(post_service)],
    session: SessionDep,
    user: CurrentUserDep,
) -> list[PostCommentResponse]:
    post_comments = post_service.get_post_comments(session, post_id=post_id)
    return [
        PostCommentResponse(
            id=post_comment.id,
            author_id=post_comment.author_id,
            post_id=post_comment.post_id,
            content=post_comment.content,
            created_at=post_comment.created_at,
            updated_at=post_comment.updated_at,
        )
        for post_comment in post_comments
    ]


@router.put("/{post_id}/comments/{comment_id}", response_model=PostCommentResponse)
async def update_post_comment(
    post_id: str,
    comment_id: str,
    body: UpdatePostCommentBody,
    post_service: Annotated[PostService, Depends(post_service)],
    session: SessionDep,
    user: CurrentUserDep,
) -> PostCommentResponse:
    post_comment = post_service.update_post_comment(
        session,
        post_id=post_id,
        comment_id=comment_id,
        content=body.content,
        author_id=user.id,
    )
    return PostCommentResponse(
        id=post_comment.id,
        author_id=post_comment.author_id,
        post_id=post_comment.post_id,
        content=post_comment.content,
        created_at=post_comment.created_at,
        updated_at=post_comment.updated_at,
    )


@router.delete(
    "/{post_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_post_comment(
    post_id: str,
    comment_id: str,
    post_service: Annotated[PostService, Depends(post_service)],
    session: SessionDep,
    user: CurrentUserDep,
) -> None:
    post_service.delete_post_comment(
        session, post_id=post_id, comment_id=comment_id, author_id=user.id
    )
