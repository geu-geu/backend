from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User


def get_user(session: Session, email: str):
    user = session.execute(
        select(User).where(
            User.email == email,
            User.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
    return user
