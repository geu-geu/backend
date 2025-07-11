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
from app.services.auth import AuthService

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

DatabaseDep = Annotated[Session, Depends(get_db)]


def get_current_user(
    db: DatabaseDep,
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
    service = AuthService(db)
    user = service.get_user_by_code(token_data.sub)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
