from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import get_db
from app.core.security import ALGORITHM
from app.models import User
from app.schemas.auth import TokenPayload
from app.services.auth import get_user_by_code

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str | None, Depends(api_key_header)],
) -> User:
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        token_type, token_value = token.split(" ")
        if token_type != "Bearer":
            raise HTTPException(status_code=401, detail="Unauthorized")
        payload = jwt.decode(token_value, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError, AttributeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    if token_data.sub is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = get_user_by_code(db, token_data.sub)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user
