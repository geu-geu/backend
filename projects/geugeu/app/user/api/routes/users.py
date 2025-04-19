from uuid import uuid4

from fastapi import APIRouter, status

from app.auth.deps import CurrentUserDep
from app.database import SessionDep
from app.user.api.schemas.users import CreateProfileImageUploadURLBody, SignupBody
from app.user.deps import UserServiceDep
from app.user.domain.user import User
from app.utils import create_presigned_url

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    body: SignupBody,
    user_service: UserServiceDep,
    session: SessionDep,
) -> User:
    return user_service.signup(session, body)


@router.get("/me")
async def me(
    user_service: UserServiceDep,
    current_user: CurrentUserDep,
    session: SessionDep,
) -> User:
    return user_service.get_user(session, current_user.id)


@router.post("/me/profile-image/upload-url")
async def create_profile_image_upload_url(
    current_user: CurrentUserDep,
    body: CreateProfileImageUploadURLBody,
):
    url = create_presigned_url(
        method="put_object",
        key=f"profile-images/{current_user.id}/{uuid4()}{body.file_extension}",
    )
    return {"url": url}
