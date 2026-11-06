
import os
import pyodbc
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_SERVER = os.getenv("DB_SERVER", r"localhost\SQLEXPRESS")
DB_NAME = os.getenv("DB_NAME")
DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server").replace(" ", "+")

engine = create_engine(
    f"mssql+pyodbc://@{DB_SERVER}/{DB_NAME}"
    f"?driver={DB_DRIVER}&trusted_connection=yes&TrustServerCertificate=yes"
)

def execute_query(query):
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df

def get_schema():
    query = """
        SELECT
            cols.table_name AS TABLE_NAME,
            cols.column_name AS COLUMN_NAME,
            cols.data_type AS DATA_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS AS cols
        WHERE cols.table_schema = 'dbo'
        ORDER BY cols.table_name, cols.ordinal_position;
    """

    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)

    return df