from typing import Any, Generator

from sqlmodel import Session, create_engine

database_url = "mssql+pyodbc://sa:Password123@localhost/streamfinity?&driver=ODBC Driver 18 for SQL Server&Encrypt=no"

engine = create_engine(
    database_url,
    echo=True,
    connect_args={"check_same_thread": False})


def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session
