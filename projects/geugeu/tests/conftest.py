import os
from collections.abc import Generator

import boto3
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.localstack import LocalStackContainer
from testcontainers.postgres import PostgresContainer

from app.api.dependencies import get_current_user
from app.core.config import settings
from app.core.db import Base, get_db
from app.core.security import get_password_hash
from app.main import app
from app.models import User


@pytest.fixture(scope="session")
def engine():
    with PostgresContainer("postgres:16") as postgres_container:
        engine = create_engine(postgres_container.get_connection_url())
        Base.metadata.create_all(engine)
        yield engine
        Base.metadata.drop_all(engine)


@pytest.fixture()
def db(engine) -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(autouse=True)
def override_get_db(db: Session):
    def get_test_db():
        yield db

    app.dependency_overrides[get_db] = get_test_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def raw_password():
    return "P@ssw0rd1234"


@pytest.fixture()
def hashed_password(raw_password):
    return get_password_hash(raw_password)


@pytest.fixture()
def user(db, hashed_password):
    user = User(
        email="user@example.com",
        password=hashed_password,
        nickname="user",
        is_admin=False,
        profile_image_url="",
    )
    db.add(user)
    db.flush()
    return user


@pytest.fixture()
def authorized_user(user):
    app.dependency_overrides[get_current_user] = lambda: user
    yield user
    app.dependency_overrides.clear()


@pytest.fixture(scope="session", autouse=True)
def localstack():
    with LocalStackContainer(
        "localstack/localstack", region_name=settings.AWS_DEFAULT_REGION
    ).with_services("s3") as container:
        original_env = {
            "AWS_ENDPOINT_URL": os.environ.get("AWS_ENDPOINT_URL"),
            "AWS_DEFAULT_REGION": os.environ.get("AWS_DEFAULT_REGION"),
        }
        endpoint_url = container.get_url()
        os.environ["AWS_ENDPOINT_URL"] = endpoint_url
        os.environ["AWS_DEFAULT_REGION"] = settings.AWS_DEFAULT_REGION

        yield container

        for key, value in original_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


@pytest.fixture(scope="session", autouse=True)
def init_s3(localstack):
    s3_client = boto3.client("s3", endpoint_url=localstack.get_url())
    s3_client.create_bucket(
        Bucket=settings.AWS_S3_BUCKET_NAME,
        CreateBucketConfiguration={"LocationConstraint": settings.AWS_DEFAULT_REGION},
    )
