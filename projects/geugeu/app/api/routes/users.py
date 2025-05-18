from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.db import get_db
from app.models import User
from app.schemas.users import SignupSchema, UserSchema, UserUpdateSchema
from app.services import users as service

router = APIRouter()


@router.post("", status_code=201, response_model=UserSchema)
async def sign_up(
    payload: SignupSchema,
    db: Annotated[Session, Depends(get_db)],
):
    return service.create_user(db, payload)


@router.get("/me", response_model=UserSchema)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.put("/me", response_model=UserSchema)
async def update_me(
    payload: UserUpdateSchema,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return service.update_user(db, current_user, payload)


@router.put("/me/profile-image", response_model=UserSchema)
async def upload_profile_image(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    file: UploadFile = File(...),
):
    return service.update_profile_image(db, current_user, file)


@router.delete("/me", status_code=204)
async def delete_me(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    service.delete_user(db, current_user)
