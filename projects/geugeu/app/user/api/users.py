from fastapi import APIRouter, status
from pydantic import BaseModel

from app.user.dependencies import UserServiceDep
from app.user.domain.user import User

router = APIRouter(prefix="/users", tags=["users"])


class SignupBody(BaseModel):
    email: str
    password: str
    name: str | None = None


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(body: SignupBody, user_service: UserServiceDep) -> User:
    return user_service.signup(email=body.email, password=body.password, name=body.name)


@router.get("/{id}")
async def get_user(id: str, user_service: UserServiceDep) -> User:
    return user_service.get_user(id=id)
