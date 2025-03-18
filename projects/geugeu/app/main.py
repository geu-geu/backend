from fastapi import FastAPI

from app.user.api import users

app = FastAPI()
app.include_router(users.router, prefix="/api")
