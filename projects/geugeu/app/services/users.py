import logging
from datetime import UTC, datetime

from fastapi import HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models import User
from app.schemas.users import SignupSchema, UserUpdateSchema
from app.utils import upload_file

logger = logging.getLogger(__name__)


def create_user(db: Session, payload: SignupSchema):
    user = db.execute(
        select(User).where(User.email == payload.email)
    ).scalar_one_or_none()
    if user:
        if user.deleted_at:
            raise HTTPException(
                status_code=400, detail="Cannot sign up with this email"
            )
        else:
            raise HTTPException(status_code=400, detail="User already exists")
    else:
        user = User(
            email=payload.email,
            nickname=payload.nickname,
            password=get_password_hash(payload.password),
            is_admin=False,
            profile_image_url="",
            auth_provider=User.AuthProvider.LOCAL,
        )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User, payload: UserUpdateSchema):
    user.nickname = payload.nickname
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User):
    user.deleted_at = datetime.now(UTC)
    db.add(user)
    db.commit()


def update_profile_image(
    db: Session,
    current_user: User,
    file: UploadFile,
):
    with db.begin_nested():
        url = upload_file(file)
        current_user.profile_image_url = url
    db.commit()
    return current_user
