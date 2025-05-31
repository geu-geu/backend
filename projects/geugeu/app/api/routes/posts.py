from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.api.dependencies import DatabaseDep, get_current_user
from app.models import User
from app.schemas.posts import PostListSchema, PostSchema
from app.services import posts as service

router = APIRouter()


@router.post("", status_code=201, response_model=PostSchema)
async def create_post(
    db: DatabaseDep,
    current_user: Annotated[User, Depends(get_current_user)],
    title: str = Form(...),
    content: str = Form(...),
    files: list[UploadFile] = File(...),
):
    return service.create_post(db, current_user, title, content, files)


@router.get("", response_model=PostListSchema)
async def get_posts(
    db: DatabaseDep,
    current_user: Annotated[User, Depends(get_current_user)],
):
    return service.get_posts(db)


@router.get("/{post_code}", response_model=PostSchema)
async def get_post(
    post_code: str,
    db: DatabaseDep,
    current_user: Annotated[User, Depends(get_current_user)],
):
    return service.get_post(db, post_code)


@router.put("/{post_code}", response_model=PostSchema)
async def update_post(
    post_code: str,
    db: DatabaseDep,
    current_user: Annotated[User, Depends(get_current_user)],
    title: str = Form(...),
    content: str = Form(...),
    files: list[UploadFile] = File(...),
):
    return service.update_post(
        db=db,
        code=post_code,
        user=current_user,
        title=title,
        content=content,
        files=files,
    )


@router.delete("/{post_code}", status_code=204)
async def delete_post(
    post_code: str,
    db: DatabaseDep,
    current_user: Annotated[User, Depends(get_current_user)],
):
    service.delete_post(db=db, code=post_code, user=current_user)
