import pyodbc

def get_sql_connection():
    conn = pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=DESKTOP-HEB09TT\\SQLEXPRESS;"
        "Database=SkyHR;"
        "Trusted_Connection=yes;"
    )
    return conn
 