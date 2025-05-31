from fastapi import APIRouter, File, UploadFile

from app.api.dependencies import CurrentUserDep, DatabaseDep
from app.schemas.users import SignupSchema, UserSchema, UserUpdateSchema
from app.services import users as service

router = APIRouter()


@router.post("", status_code=201, response_model=UserSchema)
async def sign_up(
    payload: SignupSchema,
    db: DatabaseDep,
):
    return service.create_user(db, payload)


@router.get("/me", response_model=UserSchema)
async def get_me(current_user: CurrentUserDep):
    return current_user


@router.put("/me", response_model=UserSchema)
async def update_me(
    payload: UserUpdateSchema,
    db: DatabaseDep,
    current_user: CurrentUserDep,
):
    return service.update_user(db, current_user, payload)


@router.put("/me/profile-image", response_model=UserSchema)
async def upload_profile_image(
    db: DatabaseDep,
    current_user: CurrentUserDep,
    file: UploadFile = File(...),
):
    return service.update_profile_image(db, current_user, file)


@router.delete("/me", status_code=204)
async def delete_me(
    db: DatabaseDep,
    current_user: CurrentUserDep,
):
    service.delete_user(db, current_user)
