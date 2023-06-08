import os
from typing import Any, Generator

from sqlmodel import Session, create_engine

is_testing = os.environ.get("TESTING")

database_url = "mssql+pyodbc://sa:2023streamfinity@localhost/streamfinity"

engine = create_engine(
    database_url,
    echo=True,
    connect_args={"check_same_thread": False})


def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session
