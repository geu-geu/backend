from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from app.core.config import settings
from app.core.dependencies import AuthServiceDep
from app.core.security import ALGORITHM
from app.models import User
from app.schemas.auth import TokenPayload

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


def get_current_user(
    token: Annotated[str | None, Depends(api_key_header)],
    auth_service: AuthServiceDep,
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
    user = auth_service.get_user_by_code(token_data.sub)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
