from collections.abc import Generator

from sqlmodel import Session, create_engine

from app.config import settings

engine = create_engine(str(settings.DATABASE_URL))


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
