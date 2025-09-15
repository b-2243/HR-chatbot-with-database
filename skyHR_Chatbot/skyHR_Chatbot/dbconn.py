# dbconn.py

import pyodbc
from config import SERVER, DATABASE, TRUSTED_CONNECTION

def connect_to_ssms(server=SERVER, database=DATABASE, trusted_connection=TRUSTED_CONNECTION, username=None, password=None):
    try:
        if trusted_connection:
            conn_str = (
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={server};'
                f'DATABASE={database};'
                'Trusted_Connection=yes;'
            )
        else:
            conn_str = (
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={server};'
                f'DATABASE={database};'
                f'UID={username};'
                f'PWD={password};'
            )
        print("connection successfully")    
        return pyodbc.connect(conn_str)
    except Exception as e:
        print("Connection failed:", str(e))
        return None
