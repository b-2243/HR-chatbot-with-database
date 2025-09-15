# config.py

from urllib.parse import quote_plus

SERVER = 'DESKTOP-HEB09TT\SQLEXPRESS'
DATABASE = 'SkyHR'
TRUSTED_CONNECTION = True
# API_KEY = "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"
API_KEY = "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"

ODBC_PARAMS = quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"Trusted_Connection=yes;"
)
DB_URL = f"mssql+pyodbc:///?odbc_connect={ODBC_PARAMS}"

SCHEMA_FILE_PATH = "schema_output_llm.txt"
