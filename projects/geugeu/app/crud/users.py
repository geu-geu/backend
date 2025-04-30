from datetime import UTC, datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models import User
from app.schemas.users import SignupSchema, UserUpdateSchema
from app.utils import generate_code


def create_user(session: Session, schema: SignupSchema):
    user = session.execute(
        select(User).where(User.email == schema.email)
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
            code=generate_code(),
            email=schema.email,
            nickname=schema.nickname,
            password=get_password_hash(schema.password),
            is_admin=False,
            profile_image_url="",
        )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user(session: Session, code: str):
    user = session.execute(
        select(User).where(
            User.code == code,
            User.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def update_user(session: Session, user: User, schema: UserUpdateSchema):
    user.nickname = schema.nickname
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user: User):
    user.deleted_at = datetime.now(UTC)
    session.add(user)
    session.commit()
