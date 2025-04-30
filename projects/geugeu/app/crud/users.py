from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models import User
from app.schemas.users import SignupSchema, UserUpdateSchema
from app.utils import generate_code


def create_user(session: Session, schema: SignupSchema):
    users = (
        session.execute(select(User).where(User.email == schema.email)).scalars().all()
    )
    if users:
        raise HTTPException(status_code=400, detail="User already exists")
    user = User(
        code=generate_code(),
        email=schema.email,
        nickname=schema.nickname,
        password=get_password_hash(schema.password),
        is_admin=False,
        is_active=True,
        profile_image_url=None,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user(session: Session, code: str):
    user = session.execute(
        select(User).where(User.code == code, User.is_active)
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
    user.is_active = False
    session.add(user)
    session.commit()
