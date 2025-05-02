from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.db import get_db
from app.crud import users as crud
from app.models import User
from app.schemas.users import SignupSchema, UserSchema, UserUpdateSchema

router = APIRouter()


@router.post("", status_code=201, response_model=UserSchema)
async def sign_up(
    schema: SignupSchema,
    session: Annotated[Session, Depends(get_db)],
):
    return crud.create_user(session, schema)


@router.get("/me", response_model=UserSchema)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.put("/me", response_model=UserSchema)
async def update_me(
    schema: UserUpdateSchema,
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return crud.update_user(session, current_user, schema)


@router.delete("/me", status_code=204)
async def delete_me(
    session: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    crud.delete_user(session, current_user)
