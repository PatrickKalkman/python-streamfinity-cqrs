import pyodbc
from loguru import logger
from app.db_session.db_connection_string import create_connection_string


def create_db_if_not_exists() -> None:
    conn_str = create_connection_string()
    with pyodbc.connect(conn_str) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute("SELECT name FROM master.dbo.sysdatabases WHERE name = 'streamfinity'")
            if cursor.fetchone() is None:
                logger.info("Creating database streamfinity")
                cursor.execute("CREATE DATABASE streamfinity")


def execute_sql_from_file(cursor, filename: str) -> None:
    with open(filename, 'r') as f:
        sql = f.read()
        cursor.execute(sql)


def remove_duplicate_links() -> None:
    conn_str = create_connection_string(with_database=True)
    with pyodbc.connect(conn_str) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            logger.info("Removing duplicate links")
            execute_sql_from_file(cursor, './db_session/sql/remove_duplicate_links.sql')


def create_materialized_views() -> None:
    conn_str = create_connection_string(with_database=True)
    with pyodbc.connect(conn_str) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            logger.info("Dropping materialized view if exists")
            execute_sql_from_file(cursor, './db_session/sql/drop_materialized_view.sql')

            logger.info("Creating materialized view")
            execute_sql_from_file(cursor, './db_session/sql/create_materialized_view.sql')

            logger.info("Creating materialized view's index")
            execute_sql_from_file(cursor,
                                  './db_session/sql/create_materialized_view_index.sql')
