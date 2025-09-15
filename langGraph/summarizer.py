# summarizer.py

import requests
import json

GROQ_API_KEY = "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"  

def summarize_result_with_llama(user_question, result_rows):
    if not result_rows:
        return "I can't help you with that request."

    result_text = json.dumps(result_rows, indent=2)

    prompt = f"""
You are an expert assistant. Below is a SQL query result retrieved from a database in response to the user's question.

Your job is to summarize the result in **professional, human-readable language**.
Do not return SQL code, raw tuples, or JSON objects.

If the result is empty, respond with:
"I can't help you with that request."

User question:
{user_question}

SQL Result:
{result_text}

Answer in natural language:
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You convert SQL result into natural human-readable summaries."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    result = response.json()
    final_answer = result['choices'][0]['message']['content'].strip()
    return final_answer
