from collections.abc import Generator
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.api.dependencies import get_current_user
from app.core.db import get_db
from app.main import app
from app.models import User


@pytest.fixture(scope="session")
def test_db():
    engine = create_engine(
        "sqlite:///sqlite3.db",
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


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
        id=1,
        code="abcd123",
        email="user@example.com",
        password="$2b$12$g6AeAJXUJmaOcyYwUFVqgeeDL4UOnPVPuAXjSgqmgw/ZuTztFwAe.",
        nickname="user",
        is_admin=False,
        is_active=True,
        profile_image_url=None,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    session.add(user)
    return user


@pytest.fixture()
def authorized_user(user):
    app.dependency_overrides[get_current_user] = lambda: user
    yield user
    app.dependency_overrides.clear()
