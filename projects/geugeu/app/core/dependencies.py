from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.services.auth import AuthService
from app.services.drawing_comments import DrawingCommentService
from app.services.drawings import DrawingService
from app.services.interests import InterestService
from app.services.post_comments import PostCommentService
from app.services.posts import PostService
from app.services.users import UserService

# Database dependency
DatabaseDep = Annotated[Session, Depends(get_db)]


# Service factory functions
# These create new service instances for each request with the request-scoped DB session
def get_user_service(db: DatabaseDep) -> UserService:
    return UserService(db)


def get_auth_service(db: DatabaseDep) -> AuthService:
    return AuthService(db)


def get_post_service(db: DatabaseDep) -> PostService:
    return PostService(db)


def get_drawing_service(db: DatabaseDep) -> DrawingService:
    return DrawingService(db)


def get_post_comment_service(db: DatabaseDep) -> PostCommentService:
    return PostCommentService(db)


def get_drawing_comment_service(db: DatabaseDep) -> DrawingCommentService:
    return DrawingCommentService(db)


def get_interest_service(db: DatabaseDep) -> InterestService:
    return InterestService(db)


# Service dependency annotations
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
PostServiceDep = Annotated[PostService, Depends(get_post_service)]
DrawingServiceDep = Annotated[DrawingService, Depends(get_drawing_service)]
PostCommentServiceDep = Annotated[PostCommentService, Depends(get_post_comment_service)]
DrawingCommentServiceDep = Annotated[
    DrawingCommentService, Depends(get_drawing_comment_service)
]
InterestServiceDep = Annotated[InterestService, Depends(get_interest_service)]
