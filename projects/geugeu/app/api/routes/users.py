from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.dependencies import get_current_user
from app.core.db import get_db
from app.crud.users import create_user, delete_user, update_user
from app.models import User
from app.schemas.users import SignupSchema, UserSchema, UserUpdateSchema

router = APIRouter()


@router.post("", response_model=UserSchema, status_code=201)
async def sign_up(
    schema: SignupSchema,
    session: Annotated[Session, Depends(get_db)],
):
    return create_user(session, schema)


@router.get("/me", response_model=UserSchema)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    return UserSchema(
        code=current_user.code,
        email=current_user.email,
        nickname=current_user.nickname,
        profile_image_url=current_user.profile_image_url,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )


@router.put("/me", response_model=UserSchema)
async def update_me(
    schema: UserUpdateSchema,
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return update_user(session, current_user, schema)


@router.delete("/me", status_code=204)
async def delete_me(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return delete_user(session, current_user)
