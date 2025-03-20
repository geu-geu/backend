from fastapi import FastAPI

from app.auth.api import auth
from app.user.api import users

app = FastAPI()
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
