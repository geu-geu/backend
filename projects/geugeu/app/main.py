from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.api.auth import router as auth_router
from app.drawing.api.drawings import router as drawings_router
from app.post.api.posts import router as posts_router
from app.user.api.users import router as users_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(posts_router, prefix="/api")
app.include_router(drawings_router, prefix="/api")
