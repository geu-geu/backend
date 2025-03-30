import os
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


@pytest.fixture(scope="session")
def test_db():
    engine = create_engine("sqlite:///sqlite3.db")
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)
    os.remove("sqlite3.db")


@pytest.fixture()
def session(test_db) -> Generator[Session, None, None]:
    connection = test_db.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(autouse=True)
def override_get_db(session: Session):
    def _get_db():
        yield session

    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def user():
    user = User(
        id=str(ULID()),
        email="user@example.com",
        password="password",
        is_admin=False,
        is_active=True,
    )

    def _get_current_active_user():
        return user

    app.dependency_overrides[get_current_active_user] = _get_current_active_user
    yield user
    app.dependency_overrides.clear()
