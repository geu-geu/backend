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


def create_user(session: Session, payload: SignupSchema):
    user = session.execute(
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
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update_user(session: Session, user: User, payload: UserUpdateSchema):
    user.nickname = payload.nickname
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user: User):
    user.deleted_at = datetime.now(UTC)
    session.add(user)
    session.commit()


def update_profile_image(
    session: Session,
    current_user: User,
    file: UploadFile,
):
    url = upload_file(file)
    current_user.profile_image_url = url
    session.commit()
    return current_user
