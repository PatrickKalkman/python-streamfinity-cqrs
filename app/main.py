import sys
sys.path.append("..")

import uvicorn
from fastapi import FastAPI
from sqlmodel import SQLModel
import pyodbc
from loguru import logger

import db_session.db_engine as db_engine
from routers import actors, movies, subscriptions, token, users
from app.tmdb_data_retrieval.import_movies_in_db import fill_db_with_data_if_empty


app = FastAPI(title="Streamfinity API CQRS", version="0.1.0")
app.include_router(movies.router)
app.include_router(actors.router)
app.include_router(subscriptions.router)
app.include_router(users.router)
app.include_router(token.router)

conn_str = ("Driver={ODBC Driver 18 for SQL Server};"
            "Server=localhost;"
            "UID=sa;"
            "PWD=Password123;"
            "Encrypt=no;")


def create_db_if_not_exists() -> None:
    conn = pyodbc.connect(conn_str)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM master.dbo.sysdatabases WHERE name = 'streamfinity'")
    if cursor.fetchone() is None:
        logger.info("Creating database streamfinity")
        cursor.execute("CREATE DATABASE streamfinity")
    conn.close()


def remove_duplicate_links() -> None:
    sql = ''
    logger.info("Removing duplicate links")
    with open('./remove_duplicate_links.sql', 'r') as f:
        sql = f.read()
    conn = pyodbc.connect(conn_str + "Database=streamfinity;")
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.close()


def create_materialized_views() -> None:
    sql = ''
    conn = pyodbc.connect(conn_str + "Database=streamfinity;")
    conn.autocommit = True
    cursor = conn.cursor()

    logger.info("Dropping materialized view if exists")
    with open('./drop_materialized_view.sql', 'r') as f:
        sql = f.read()
    cursor.execute(sql)

    logger.info("Creating materialized view if exists")
    with open('./create_materialized_view.sql', 'r') as f:
        sql = f.read()
    cursor.execute(sql)

    logger.info("Creating materialized views index")
    with open('./create_materialized_view_index.sql', 'r') as f:
        sql = f.read()
    cursor.execute(sql)

    conn.close()


@app.on_event("startup")
def on_startup() -> None:
    create_db_if_not_exists()
    SQLModel.metadata.create_all(db_engine.engine)
    fill_db_with_data_if_empty()
    remove_duplicate_links()
    create_materialized_views()


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
