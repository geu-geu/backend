from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from app.core.config import settings
from app.core.dependencies import AuthServiceDep
from app.core.security import ALGORITHM
from app.models import User
from app.schemas.auth import TokenPayload

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


def get_current_user_optional(
    token: Annotated[str | None, Depends(api_key_header)],
    auth_service: AuthServiceDep,
) -> User | None:
    if not token:
        return None
    try:
        token_type, token_value = token.split(" ")
        if token_type != "Bearer":
            return None
        payload = jwt.decode(token_value, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError, AttributeError, ValueError):
        return None
    if token_data.sub is None:
        return None
    user = auth_service.get_user_by_code(token_data.sub)
    return user


def get_current_user(
    user: Annotated[User | None, Depends(get_current_user_optional)],
) -> User:
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
CurrentUserOptionalDep = Annotated[User | None, Depends(get_current_user_optional)]
