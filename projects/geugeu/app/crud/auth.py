from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User


def get_user(session: Session, email: str):
    user = session.execute(
        select(User).where(
            User.email == email,
            User.is_active,
        )
    ).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
