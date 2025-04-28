from collections.abc import Generator

from sqlmodel import Session, create_engine

from app.core.config import settings

engine = create_engine(str(settings.POSTGRES_DATABASE_URL))


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
