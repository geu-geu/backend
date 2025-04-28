from datetime import UTC, datetime

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models import User
from app.schemas.users import SignupSchema
from app.utils import generate_code


def create_user(session: Session, schema: SignupSchema):
    users = session.exec(select(User).where(User.email == schema.email)).fetchall()
    if users:
        raise HTTPException(status_code=400, detail="User already exists")
    user = User(
        code=generate_code(),
        email=schema.email,
        name=schema.name,
        password=schema.password,
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
