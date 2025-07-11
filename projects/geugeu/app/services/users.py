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


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, payload: SignupSchema) -> User:
        user = self.db.execute(
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
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user: User, payload: UserUpdateSchema) -> User:
        user.nickname = payload.nickname
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user: User) -> None:
        user.deleted_at = datetime.now(UTC)
        self.db.add(user)
        self.db.commit()

    def update_profile_image(self, current_user: User, file: UploadFile) -> User:
        with self.db.begin_nested():
            url = upload_file(file)
            current_user.profile_image_url = url
        self.db.commit()
        return current_user
