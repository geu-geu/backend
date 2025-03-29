from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel
from ulid import ULID

from app.auth.dependencies import get_current_active_user
from app.auth.domain.user import User
from app.database import get_db
from app.main import app


@pytest.fixture(autouse=True)
def session() -> Generator[Session, None, None]:
    _engine = create_engine("sqlite:///sqlite3.db")
    SQLModel.metadata.create_all(_engine)
    with Session(_engine) as session:
        yield session
    SQLModel.metadata.drop_all(_engine)


@pytest.fixture(autouse=True)
def override_get_db(session: Session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def user() -> User:
    return User(
        id=str(ULID()),
        email="test@example.com",
        password="password",
        is_active=True,
        is_admin=False,
    )


@pytest.fixture(autouse=True)
def override_auth_dependency():
    def override_current_active_user_dep():
        return User(
            id=str(ULID()),
            email="user@example.com",
            password="password",
            is_admin=False,
            is_active=True,
        )

    app.dependency_overrides[get_current_active_user] = override_current_active_user_dep
    yield
    app.dependency_overrides.clear()
