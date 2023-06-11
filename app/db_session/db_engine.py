from typing import Any, Generator

from sqlmodel import Session, create_engine
from app.db_session.db_connection_string import create_engine_string

engine = create_engine(
    create_engine_string(),
    echo=True,
    connect_args={"check_same_thread": False})


def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session
