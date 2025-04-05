from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.deps import auth_service
from app.auth.services.auth_service import AuthService
from app.database import SessionDep

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(auth_service)],
    session: SessionDep,
):
    return auth_service.login(
        session, email=form_data.username, password=form_data.password
    )
