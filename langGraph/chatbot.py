from db_conn import get_sql_connection
from query_generator import generate_sql_from_llama
from summarizer import summarize_result_with_llama
from datetime import datetime, date

def serialize_row(row_dict):
    return {
        k: (v.isoformat() if isinstance(v, (datetime, date)) else v)
        for k, v in row_dict.items()
    }

def ask_chatbot(user_question):
    print("🤖 Generating SQL for:", user_question)
    PersonId = '0A6EFDC5-A31B-47F3-AEDE-B149B845AA69'
    sql_query = generate_sql_from_llama(user_question,PersonId)
    print("🧠 Generated SQL:", sql_query)

    conn = get_sql_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        raw_results = [dict(zip(columns, row)) for row in rows]
        results = [serialize_row(row) for row in raw_results]
    except Exception as e:
        return f"I can't help you with that request. (Error: {str(e)})"
    finally:
        conn.close()

    return summarize_result_with_llama(user_question, results)
