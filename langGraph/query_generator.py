# # query_generator.py
# import requests
# from schema_graph import get_table_relationships

# GROQ_API_KEY = "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"  # 🔐 Replace this with your actual Groq API key

# def clean_llm_output(output):
#     """
#     Cleans LLM output by removing backticks and code block markers.
#     """
#     output = output.strip()
#     if output.startswith("```"):
#         output = output.strip("`")
#         if output.lower().startswith("sql"):
#             output = output[3:].strip()
#     return output.strip("`").strip()

# def generate_sql_from_llama(user_question):
#     schema_context = get_table_relationships()

#     prompt = f"""
# You are an expert SQL assistant. Given the database schema relationships and a user question, generate a valid SQL Server query.

# Schema relationships:
# {schema_context}

# Question:
# {user_question}

# Respond ONLY with the SQL query. Do NOT include ```sql or any explanations.
# """

#     url = "https://api.groq.com/openai/v1/chat/completions"
#     headers = {
#         "Authorization": f"Bearer {GROQ_API_KEY}",
#         "Content-Type": "application/json"
#     }
#     data = {
#         "model": "llama3-70b-8192",
#         "messages": [
#             {"role": "system", "content": "You generate SQL Server queries only. No markdown or explanation."},
#             {"role": "user", "content": prompt}
#         ],
#         "temperature": 0.1
#     }

#     response = requests.post(url, headers=headers, json=data)
#     result = response.json()
#     raw_sql = result['choices'][0]['message']['content'].strip()
#     return clean_llm_output(raw_sql)
 
 
import requests
from schema_graph import get_filtered_table_paths

GROQ_API_KEY = "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"

def clean_llm_output(output):
    output = output.strip()
    if output.startswith("```"):
        output = output.strip("`")
        if output.lower().startswith("sql"):
            output = output[3:].strip()
    return output.strip("`").strip()

def generate_sql_from_llama(user_question,PersonId):
    # Use full multi-hop foreign key paths
    schema_context = get_filtered_table_paths()
    print("schema_context",schema_context)
    
    prompt = f"""
You are an expert SQL assistant. Below are multi-table foreign key relationships in the database.

Each line represents a link: 
    TableA.column → TableB.column

### Schema foreign key relationships:
{schema_context}

### Question:
{user_question}
You may only use the following tables in your answer:
PolicyType, Organizations, CompanyPolicy, Persons, PersonFamilyDetails, PersonExperiences, PersonEducations, PersonDocument

❗"Only return the SQL query, nothing else."


### Important rules:
1. If the question involves any table not listed above, respond with: I can't help you with that request.
2. If the question involves any of these tables:
   PersonFamilyDetails, PersonExperiences, PersonEducations, PersonDocument,
   Attendances, AttendanceDetails
   then filter the results by: PersonId = '{PersonId}'
3. If the question involves the Persons table, then filter the results by: Id = '{PersonId}'

Now write a valid SQL Server query to answer the question below, using appropriate joins.

### Instructions:
- Only use the tables and columns provided in the schema above.
- Use JOINs only if needed and valid.
- Do NOT make up any table or column names.
- Do NOT explain anything. Return only the final SQL SELECT query.
- Output only valid SQL.
### SQL Query:

Output only the SQL query or the exact message: I can't help you with that request.
Do not include markdown, explanations, or any formatting.
"""



    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You generate SQL Server queries only. No markdown or explanation."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

    result = response.json()
    raw_sql = result['choices'][0]['message']['content'].strip()
    return clean_llm_output(raw_sql)
