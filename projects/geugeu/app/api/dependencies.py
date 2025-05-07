from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import get_db
from app.core.security import ALGORITHM
from app.crud.auth import get_user_by_code
from app.models import User
from app.schemas.auth import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    session: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(reusable_oauth2)],
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    if token_data.sub is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = get_user_by_code(session, token_data.sub)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user
