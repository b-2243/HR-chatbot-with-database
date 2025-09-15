# tools_setup.py

from langchain.tools import Tool
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from query_generation import query_ssms_with_context, llm
from config import DB_URL

ssms_query_tool = Tool(
    name="SSMSQueryTool",
    func=query_ssms_with_context,
    description="Use this tool to query SQL Server database using SQL. Input should be a valid SQL SELECT statement."
)

sql_db = SQLDatabase.from_uri(DB_URL)
sql_toolkit = SQLDatabaseToolkit(db=sql_db, llm=llm)
sql_tools = sql_toolkit.get_tools()
