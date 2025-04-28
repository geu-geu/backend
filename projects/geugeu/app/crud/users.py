from datetime import UTC, datetime

from fastapi import HTTPException
from sqlmodel import Session, select

from app.core.security import get_password_hash
from app.models import User
from app.schemas.users import SignupSchema, UserUpdateSchema
from app.utils import generate_code


def create_user(session: Session, schema: SignupSchema):
    users = session.exec(select(User).where(User.email == schema.email)).fetchall()
    if users:
        raise HTTPException(status_code=400, detail="User already exists")
    user = User(
        code=generate_code(),
        email=schema.email,
        name=schema.name,
        password=get_password_hash(schema.password),
        is_admin=False,
        is_active=True,
        profile_image_url=None,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user(session: Session, code: str):
    user = session.exec(select(User).where(User.code == code, User.is_active)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def update_user(session: Session, user: User, schema: UserUpdateSchema):
    user.name = schema.name
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user: User):
    user.is_active = False
    session.add(user)
    session.commit()
