from fastapi import APIRouter

from app.api.routes import drawing_comments, drawings, post_comments, posts, users

api_router = APIRouter()

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
)
api_router.include_router(
    posts.router,
    prefix="/posts",
    tags=["posts"],
)
api_router.include_router(
    drawings.router,
    prefix="/drawings",
    tags=["drawings"],
)
api_router.include_router(
    post_comments.router,
    prefix="/posts",
    tags=["post-comments"],
)
api_router.include_router(
    drawing_comments.router,
    prefix="/drawings",
    tags=["drawing-comments"],
)
