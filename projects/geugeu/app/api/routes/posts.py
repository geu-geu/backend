from typing import Annotated

from fastapi import APIRouter, File, Form, Query, UploadFile

from app.api.dependencies import CurrentUserDep
from app.core.dependencies import PostServiceDep
from app.schemas.posts import PostListFilter, PostListSchema, PostSchema

router = APIRouter()


@router.post("", status_code=201, response_model=PostSchema)
async def create_post(
    current_user: CurrentUserDep,
    service: PostServiceDep,
    title: str = Form(...),
    content: str = Form(...),
    files: list[UploadFile] = File(...),
):
    return service.create_post(current_user, title, content, files)


@router.get("", response_model=PostListSchema)
async def get_posts(
    current_user: CurrentUserDep,
    service: PostServiceDep,
    filters: Annotated[PostListFilter, Query()],
):
    return service.get_posts(filters)


@router.get("/{post_code}", response_model=PostSchema)
async def get_post(
    post_code: str,
    current_user: CurrentUserDep,
    service: PostServiceDep,
):
    return service.get_post(post_code)


@router.put("/{post_code}", response_model=PostSchema)
async def update_post(
    post_code: str,
    current_user: CurrentUserDep,
    service: PostServiceDep,
    title: str = Form(...),
    content: str = Form(...),
    files: list[UploadFile] = File(...),
):
    return service.update_post(
        code=post_code,
        user=current_user,
        title=title,
        content=content,
        files=files,
    )


@router.delete("/{post_code}", status_code=204)
async def delete_post(
    post_code: str,
    current_user: CurrentUserDep,
    service: PostServiceDep,
):
    service.delete_post(code=post_code, user=current_user)
