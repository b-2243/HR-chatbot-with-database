# query_generation.py
from langchain.tools import Tool
from sentence_transformers import SentenceTransformer, util
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent
from dbconn import connect_to_ssms
from config import DB_URL
from schema_utils import load_schema_text, parse_schema_to_table_blocks
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents.output_parsers import ReActSingleInputOutputParser
# from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun
# from langchain_community.utilities import WikipediaAPIWrapper,ArxivAPIWrapper
import faiss
import os
import numpy as np

VECTOR_DB_PATH = "schema_faiss_index"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
SCHEMA_FILE = "schema_output_llm.txt"

def build_agent(api_key: str):
    llm = ChatGroq(api_key=api_key, model_name="llama3-70b-8192", streaming=True)
    schema_text = load_schema_text("updated_schema_output_llm.txt")
    schema = parse_schema_to_table_blocks(schema_text)
    table_names = list(schema.keys())
    table_descriptions = list(schema.values())

    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    dimension = 384
    if os.path.exists(f"{VECTOR_DB_PATH}.index") and os.path.exists(f"{VECTOR_DB_PATH}_meta.npy"):
        # Load FAISS index and metadata
        faiss_index = faiss.read_index(f"{VECTOR_DB_PATH}.index")
        table_names = np.load(f"{VECTOR_DB_PATH}_meta.npy", allow_pickle=True).tolist()
    else:
        # First-time: create FAISS index and save it
        embeddings = model.encode(table_descriptions, convert_to_numpy=True).astype('float32')
        faiss_index = faiss.IndexFlatL2(dimension)
        faiss_index.add(embeddings)
        faiss.write_index(faiss_index, f"{VECTOR_DB_PATH}.index")
        np.save(f"{VECTOR_DB_PATH}_meta.npy", np.array(table_names))
    # schema_embeddings = model.encode(table_descriptions, convert_to_tensor=True)

    # def get_relevant_tables(question: str, top_n=10):
    #     question_embedding = model.encode(question, convert_to_tensor=True)
    #     similarities = util.cos_sim(question_embedding, schema_embeddings)[0]
    #     top_indices = similarities.argsort(descending=True)[:top_n]
    #     return [table_names[i] for i in top_indices]
    
    def get_relevant_tables(question: str, top_n=10):
        question_embedding = model.encode(question, convert_to_numpy=True).astype('float32').reshape(1, -1)
        _, top_indices = faiss_index.search(question_embedding, top_n)
        return [table_names[i] for i in top_indices[0]]

    def query_ssms_with_context(natural_question: str) -> str:
        relevant_tables = get_relevant_tables(natural_question)
        print("relevant_tables",relevant_tables)
        context_blocks = [schema[table] for table in relevant_tables if table in schema]
        schema_context = "\n\n".join(context_blocks)

        prompt = f"""
You are an expert SQL query generator. Based only on the tables and columns listed below, write a syntactically correct and semantically accurate SQL SELECT query that answers the given question.

### Available Schema:
{schema_context}

### Question:
{natural_question}

### Instructions:
- Only use the tables and columns provided in the schema above.
- Use appropriate JOINs based on column/foreign key relationships if needed.
- Do NOT make up any table or column names.
- Do NOT explain anything; return only the final SQL SELECT query.
- Only use tables listed in the schema below.
- If a person's name is queried, refer to the `Persons` table where `FirstName` and `LastName` exist (if applicable).
- If the question cannot be answered using the provided schema, respond with: "No data found in the database for the given input."

### Output:
"""
        sql_query = llm.invoke(prompt).content.strip().replace("`", "")
        conn = connect_to_ssms()
        if conn is None:
            return "Connection failed."

        try:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            return (
                f"Top relevant tables: {', '.join(relevant_tables)}\n"
                f"SQL Generated:\n{sql_query}\n\n"
                f"Query Result:\n{result}"
            )
        except Exception as e:
            return f"Error executing query: {str(e)}"
        finally:
            conn.close()

    ssms_query_tool = Tool(
        name="SSMSQueryTool",
        func=query_ssms_with_context,
        description="Use this tool to query the SQL Server database. Input must be a valid SQL SELECT statement. The tool returns only formatted results, not the query.Use this tool ONLY IF the default SQL tools fail or are unable to retrieve data."
    )

    sql_db = SQLDatabase.from_uri(DB_URL)
    sql_toolkit = SQLDatabaseToolkit(db=sql_db, llm =llm)
    sql_tools = sql_toolkit.get_tools()
   

    prefix = """
    You are an assistant that helps retrieve data from a SQL Server database.
    You MUST use the tools provided to execute SQL queries and return ONLY the results.
    - Use the default SQL_tools (like `sql_db_query`) to generate and execute queries whenever possible.
    - If the default tools fail or return no data, use `SSMSQueryTool` as a fallback to execute the actual SQL against the database.

    NEVER show the raw SQL query in your final answer.
    If the result is empty, just respond: "No data found in the database for the given input."

    After retrieving the result, respond in **clear and professional natural language**.

    Avoid showing any raw data structures like tuples, lists, or SQL queries.
    Only provide the final answer in a human-readable format.

    If no result is found, respond with:
    "No data found in the database for the given input."
    """

    agent = initialize_agent(
        tools= [ssms_query_tool],
        llm=llm,
        agent_type="zero-shot-react-description",
        verbose=True,
        handle_parsing_errors=True,
        output_parser=ReActSingleInputOutputParser(),
        agent_kwargs={"prefix": prefix}
    )
    return agent




 # api_wrapper_wiki = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=250)
    # wiki_tool  = WikipediaQueryRun(api_wrapper=api_wrapper_wiki)
    # wiki_tool.name

    # api_wrapper_arxiv = ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=250)
    # arxiv_tool  = ArxivQueryRun(api_wrapper=api_wrapper_arxiv)
    # arxiv_tool.name
    
    
#     prefix = """
# You are an intelligent assistant that can:
# - Answer general knowledge questions using Wikipedia.
# - Fetch scientific research using Arxiv.
# - Query a SQL Server database using either:
#   • SSMSQueryTool: a custom tool that uses semantic search and schema context to generate and run SQL queries.
#   • SQL_tools: inbuilt LangChain tools for direct database interaction using structured prompts.

# Choose the appropriate tool based on the user's question.

# Instructions:
# - For natural language database questions, prefer SSMSQueryTool.
# - For direct or structured SQL questions, use the SQL_tools.
# - For general topics, use Wikipedia.
# - For research or academic content, use Arxiv.

# Respond in **clear, human-readable language**.
# NEVER expose raw SQL queries, Python data structures (like lists or dicts), or code unless explicitly requested.
# If a SQL query returns an empty result, respond with:
# "No data found in the database for the given input."
# If no result is found, respond with:
# "No data found in the database for the given input."
# """    