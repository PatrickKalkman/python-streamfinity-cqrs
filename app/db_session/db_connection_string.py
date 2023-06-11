import os
from dotenv import load_dotenv

load_dotenv()

SQL_USERNAME = os.getenv('SQL_USERNAME', 'sa')
SQL_PASSWORD = os.getenv('SQL_PASSWORD', 'ULpxRKtTH5rqXivrLG77')


def create_connection_string(with_database: bool = False) -> str:

    conn_str = ("Driver={ODBC Driver 18 for SQL Server};"
                "Server=localhost;"
                f"UID={SQL_USERNAME};"
                f"PWD={SQL_PASSWORD};"
                "Encrypt=no;")
    return conn_str if not with_database else conn_str + "Database=streamfinity;"


def create_engine_string() -> str:
    return ("mssql+pyodbc://"
            f"{SQL_USERNAME}:{SQL_PASSWORD}"
            "@localhost/streamfinity"
            "?&driver=ODBC Driver 18 for SQL Server&Encrypt=no")
