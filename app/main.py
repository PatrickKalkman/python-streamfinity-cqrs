import sys
sys.path.append("..")

import uvicorn
from fastapi import FastAPI
from sqlmodel import SQLModel
import pyodbc
from loguru import logger

import db_session.db_engine as db_engine
from routers import actors, movies, subscriptions, token, users

app = FastAPI(title="Streamfinity API CQRS", version="0.1.0")
app.include_router(movies.router)
app.include_router(actors.router)
app.include_router(subscriptions.router)
app.include_router(users.router)
app.include_router(token.router)


def create_db_if_not_exists() -> None:
    conn_str = ("Driver={ODBC Driver 18 for SQL Server};"
                "Server=localhost;"
                "UID=sa;"
                "PWD=Password123;"
                "Encrypt=no;")
    conn = pyodbc.connect(conn_str)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM master.dbo.sysdatabases WHERE name = 'streamfinity'")
    if cursor.fetchone() is None:
        cursor.execute("CREATE DATABASE streamfinity")
    conn.close()




@app.on_event("startup")
def on_startup() -> None:
    create_db_if_not_exists()
    SQLModel.metadata.create_all(db_engine.engine)


if __name__ == "__main__":
    conn_str = ("Driver={ODBC Driver 18 for SQL Server};"
                "Server=localhost;"
                "UID=sa;"
                "PWD=Password123;"
                "Encrypt=no;")
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    logger.info(cursor.execute("SELECT @@version;").fetchone()[0])
    conn.close()
    uvicorn.run(app, reload=True)
