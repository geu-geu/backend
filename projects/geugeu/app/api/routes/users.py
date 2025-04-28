from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.db import get_db
from app.crud.users import create_user
from app.schemas.users import SignupSchema, UserSchema

router = APIRouter()


@router.post("", response_model=UserSchema, status_code=201)
async def sign_up(
    schema: SignupSchema,
    session: Annotated[Session, Depends(get_db)],
):
    return create_user(session, schema)


@router.get("/me")
async def get_me():
    raise NotImplementedError


@router.put("/me")
async def update_me():
    raise NotImplementedError


@router.delete("/me")
async def delete_me():
    raise NotImplementedError
