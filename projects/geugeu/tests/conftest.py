from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from app.api.dependencies import get_current_user
from app.core.db import Base, get_db
from app.main import app
from app.models import User


@pytest.fixture(scope="session")
def test_db():
    with PostgresContainer("postgres:16") as postgres_container:
        engine = create_engine(postgres_container.get_connection_url())
        Base.metadata.create_all(engine)
        yield engine
        Base.metadata.drop_all(engine)


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
    def get_test_db():
        yield session

    app.dependency_overrides[get_db] = get_test_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def user(session):
    user = User(
        code="abcd123",
        email="user@example.com",
        password="$2b$12$g6AeAJXUJmaOcyYwUFVqgeeDL4UOnPVPuAXjSgqmgw/ZuTztFwAe.",
        nickname="user",
        is_admin=False,
        profile_image_url="",
    )
    session.add(user)
    session.flush()
    return user


@pytest.fixture()
def authorized_user(user):
    app.dependency_overrides[get_current_user] = lambda: user
    yield user
    app.dependency_overrides.clear()
