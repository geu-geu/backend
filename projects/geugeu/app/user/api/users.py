from fastapi import APIRouter, status
from pydantic import BaseModel

from app.user.application.user_service import UserService
from app.user.domain.entity.user import User
from app.user.infrastructure.repository.user_repository import UserRepository

router = APIRouter(prefix="/users", tags=["users"])


class SignupBody(BaseModel):
    email: str
    password: str
    name: str | None = None


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(body: SignupBody) -> User:
    user_repository = UserRepository()
    user_service = UserService(user_repository=user_repository)
    user = user_service.signup(email=body.email, password=body.password, name=body.name)
    return user
