from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.dependencies import get_current_user
from app.core.db import get_db
from app.crud.users import create_user, update_user
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
    return current_user


@router.put("/me", response_model=UserSchema)
async def update_me(
    schema: UserUpdateSchema,
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return update_user(session, current_user, schema)


@router.delete("/me")
async def delete_me():
    raise NotImplementedError
