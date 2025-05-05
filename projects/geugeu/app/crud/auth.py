from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User


def get_user_by_code(session: Session, code: str) -> User | None:
    return session.execute(
        select(User).where(
            User.code == code,
            User.deleted_at.is_(None),
        )
    ).scalar_one_or_none()


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.execute(
        select(User).where(
            User.email == email,
            User.deleted_at.is_(None),
        )
    ).scalar_one_or_none()
