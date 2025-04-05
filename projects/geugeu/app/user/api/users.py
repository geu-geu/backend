from fastapi import APIRouter, status
from pydantic import BaseModel

from app.auth.deps import CurrentUserDep
from app.database import SessionDep
from app.user.deps import UserServiceDep
from app.user.domain.user import User

router = APIRouter(prefix="/users", tags=["users"])


class SignupBody(BaseModel):
    email: str
    password: str
    name: str | None = None


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    body: SignupBody,
    user_service: UserServiceDep,
    session: SessionDep,
) -> User:
    return user_service.signup(
        session, email=body.email, password=body.password, name=body.name
    )


@router.get("/me")
async def me(
    user_service: UserServiceDep,
    current_user: CurrentUserDep,
    session: SessionDep,
) -> User:
    return user_service.get_user(session, current_user.id)
