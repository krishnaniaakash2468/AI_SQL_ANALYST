
import os
import pyodbc
import pandas as pd
from sqlalchemy import create_engine, text
from langchain.tools import tool
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
load_dotenv()
load_dotenv(os.path.join(HERE, "_env"))  # optional alternative env file name

DB_SERVER = os.getenv("DB_SERVER", r"localhost\SQLEXPRESS")
DB_NAME = os.getenv("DB_NAME")
DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server").replace(" ", "+")

engine = create_engine(
    f"mssql+pyodbc://@{DB_SERVER}/{DB_NAME}"
    f"?driver={DB_DRIVER}&trusted_connection=yes&TrustServerCertificate=yes"
)
@tool
def execute_query(query):
    """ use this tool to execute a SQL query and return the result"""
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df
@tool
def get_schema():
    """ use this tool to get the schema of all the tables in the database"""
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