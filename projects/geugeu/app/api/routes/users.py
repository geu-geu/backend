from fastapi import APIRouter, File, UploadFile

from app.api.dependencies import CurrentUserDep, DatabaseDep
from app.schemas.users import SignupSchema, UserSchema, UserUpdateSchema
from app.services.users import UserService

router = APIRouter()


@router.post("", status_code=201, response_model=UserSchema)
async def sign_up(
    payload: SignupSchema,
    db: DatabaseDep,
):
    service = UserService(db)
    return service.create_user(payload)


@router.get("/me", response_model=UserSchema)
async def get_me(current_user: CurrentUserDep):
    return current_user


@router.put("/me", response_model=UserSchema)
async def update_me(
    payload: UserUpdateSchema,
    db: DatabaseDep,
    current_user: CurrentUserDep,
):
    service = UserService(db)
    return service.update_user(current_user, payload)


@router.put("/me/profile-image", response_model=UserSchema)
async def upload_profile_image(
    db: DatabaseDep,
    current_user: CurrentUserDep,
    file: UploadFile = File(...),
):
    service = UserService(db)
    return service.update_profile_image(current_user, file)


@router.delete("/me", status_code=204)
async def delete_me(
    db: DatabaseDep,
    current_user: CurrentUserDep,
):
    service = UserService(db)
    service.delete_user(current_user)
