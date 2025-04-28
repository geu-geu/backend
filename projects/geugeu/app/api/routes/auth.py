from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.core.db import get_db
from app.core.security import create_access_token, verify_password
from app.models import User
from app.schemas.auth import Token

router = APIRouter()


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_db)],
):
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return Token(
        access_token=create_access_token(user.code, expires_delta=timedelta(days=1)),
        token_type="Bearer",
    )
