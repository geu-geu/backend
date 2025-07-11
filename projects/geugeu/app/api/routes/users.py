from fastapi import APIRouter, File, UploadFile

from app.api.dependencies import CurrentUserDep
from app.core.dependencies import UserServiceDep
from app.schemas.users import SignupSchema, UserSchema, UserUpdateSchema

router = APIRouter()


@router.post("", status_code=201, response_model=UserSchema)
async def sign_up(
    payload: SignupSchema,
    service: UserServiceDep,
):
    return service.create_user(payload)


@router.get("/me", response_model=UserSchema)
async def get_me(current_user: CurrentUserDep):
    return current_user


@router.put("/me", response_model=UserSchema)
async def update_me(
    payload: UserUpdateSchema,
    current_user: CurrentUserDep,
    service: UserServiceDep,
):
    return service.update_user(current_user, payload)


@router.put("/me/profile-image", response_model=UserSchema)
async def upload_profile_image(
    current_user: CurrentUserDep,
    service: UserServiceDep,
    file: UploadFile = File(...),
):
    return service.update_profile_image(current_user, file)


@router.delete("/me", status_code=204)
async def delete_me(
    current_user: CurrentUserDep,
    service: UserServiceDep,
):
    service.delete_user(current_user)
