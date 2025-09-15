import pyodbc
import re
import os
from sentence_transformers import SentenceTransformer, util
from langchain_groq import ChatGroq
from chatbotmodule.serializers import ChatbotSerializer
from rest_framework.views import APIView
from chatbotmodule.logger_function import logger_function
from django.conf import settings
from rest_framework.response import Response
from chatbotmodule.utils.prompts_loader import get_formatted_prompt
from rest_framework import status
from chatbotmodule.db_connection import getConnection
from langchain_core.messages import AIMessage


filename=os.path.basename(__file__)[:-3]

# api_key = "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"
api_key = "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"

llm = ChatGroq(api_key=api_key, model_name="llama3-70b-8192", streaming=False)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'model_files', 'all-MiniLM-L6-v2')
model = SentenceTransformer(MODEL_PATH)

def load_schema_text(file_path: str) -> str:
    with open(file_path, 'r', encoding="utf-8") as f:
        return f.read()



def parse_schema_to_table_blocks(schema_text: str) -> dict:
    blocks = schema_text.strip().split('\n\n')
    table_blocks = {}
    for block in blocks:
        lines = block.strip().splitlines()
        if not lines:
            continue
        match = re.match(r"^([A-Za-z0-9_]+):", lines[0])
        if match:
            table_name = match.group(1)
            table_blocks[table_name] = block.strip()
    return table_blocks


# schema_text = load_schema_text("D:\hrchatbot\hrchatbot\chatbotmodule\schema_output_llm.txt")
# schema = parse_schema_to_table_blocks(schema_text)
# table_names = list(schema.keys())
# table_descriptions = list(schema.values())
# schema_embeddings = model.encode(table_descriptions, convert_to_tensor=True)





# def get_relevant_tables(question: str, top_n=3):
#     question_embedding = model.encode(question, convert_to_tensor=True)
#     similarities = util.cos_sim(question_embedding, schema_embeddings)[0]
#     top_indices = similarities.argsort(descending=True)[:top_n]
#     return [table_names[i] for i in top_indices]

def query_ssms_with_context_personal_details(natural_question: str,status:int) -> str:
    try:
        natural_question, PersonId = [x.strip() for x in natural_question.split("|", 1)]
    except ValueError:
        return " Invalid input. Use format: 'question | PersonId'"
    
    
    schema_text = load_schema_text("D:\hrchatbot\hrchatbot\chatbotmodule\schema_output_llm.txt")
    schema = parse_schema_to_table_blocks(schema_text)
    table_names = list(schema.keys())
    table_descriptions = list(schema.values())
    schema_embeddings = model.encode(table_descriptions, convert_to_tensor=True)

    def get_relevant_tables(question: str, top_n=3):
        question_embedding = model.encode(question, convert_to_tensor=True)
        similarities = util.cos_sim(question_embedding, schema_embeddings)[0]
        top_indices = similarities.argsort(descending=True)[:top_n]
        return [table_names[i] for i in top_indices]

    relevant_tables = get_relevant_tables(natural_question)
    context_blocks = [schema[table] for table in relevant_tables if table in schema]
    schema_context = "\n\n".join(context_blocks)

    try:
        prompt=get_formatted_prompt(f"status_{status}",schema_context=schema_context, natural_question=natural_question, PersonId=PersonId)
        logger_function(filename,prompt,1)
    except Exception as e:
        logger_function(filename,f"Prompt formatting error:{str(e)}",2)
        # return False
    try:
        sql_query = llm.invoke(prompt).content.strip().replace("`", "")
        logger_function(filename,sql_query,1)
    except Exception as e:
        logger_function(filename,f" LLM Error: {str(e)}",2)
        return False

    os.makedirs("logs", exist_ok=True)
    with open("logs/prompt_log.txt", "a", encoding="utf-8") as f:
        f.write(f"\n---\nPrompt:\n{prompt}\nSQL:\n{sql_query}\n")
        
    server= settings.DATABASES['default']['HOST']
    print(server)
    database=settings.DATABASES['default']['NAME']
    print(database)
    
    conn = getConnection()
    if conn is None:
        logger_function(filename,e,2)
        return " Failed to connect to the database."

    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]

        # if result:
        #     answer = ", ".join(f"{k}: {v}" for k, v in result[0].items())
        #     logger_function(filename,answer,1)
        #     return answer
        # else:
        #     return "No data found for the provided ID."

        if result:
            all_answers = []
            for row in result:
                row_str = ", ".join(f"{k}: {v}" for k, v in row.items())
                all_answers.append(f"[{row_str}]")
            answer = " | ".join(all_answers)  
            return f"Answer: {answer}"
        else:
            return "No data found for the provided ID."
        
    except Exception as e:
        return f"Error executing SQL:\n{sql_query}\n\nError: {str(e)}"
    finally:
        conn.close()


def query_ssms_with_context_company_policy(natural_question: str,status:int) -> str:
    # try:
    #     natural_question, PersonId = [x.strip() for x in natural_question.split("|", 1)]
    # except ValueError:
    #     return " Invalid input. Use format: 'question | PersonId'"
    
    schema_text = load_schema_text("D:\hrchatbot\hrchatbot\chatbotmodule\company_policy.txt")
    schema = parse_schema_to_table_blocks(schema_text)
    table_names = list(schema.keys())
    table_descriptions = list(schema.values())
    schema_embeddings = model.encode(table_descriptions, convert_to_tensor=True)

    def get_relevant_tables(question: str, top_n=3):
        question_embedding = model.encode(question, convert_to_tensor=True)
        similarities = util.cos_sim(question_embedding, schema_embeddings)[0]
        top_indices = similarities.argsort(descending=True)[:top_n]
        return [table_names[i] for i in top_indices]

    relevant_tables = get_relevant_tables(natural_question)
    context_blocks = [schema[table] for table in relevant_tables if table in schema]
    schema_context = "\n\n".join(context_blocks)


    try:
        prompt=get_formatted_prompt(f"status_{status}",schema_context=schema_context, natural_question=natural_question)
        logger_function(filename,prompt,1)
    except Exception as e:
        logger_function(filename,f"Prompt formatting error:{str(e)}",2)
        # return False
    try:
        sql_query = llm.invoke(prompt).content.strip().replace("`", "")
        logger_function(filename,sql_query,1)
    except Exception as e:
        logger_function(filename,f" LLM Error: {str(e)}",2)
        return False

    os.makedirs("logs", exist_ok=True)
    with open("logs/prompt_log.txt", "a", encoding="utf-8") as f:
        f.write(f"\n---\nPrompt:\n{prompt}\nSQL:\n{sql_query}\n")
        
    server= settings.DATABASES['default']['HOST']
    print(server)
    database=settings.DATABASES['default']['NAME']
    print(database)
    
    conn = getConnection()
    if conn is None:
        logger_function(filename,e,2)
        return " Failed to connect to the database."

    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]

        # if result:
        #     answer = ", ".join(f"{k}: {v}" for k, v in result[0].items())
        #     logger_function(filename,answer,1)
        #     return answer
        # else:
        #     return "No data found for the provided ID."

        if result:
            all_answers = []
            for row in result:
                row_str = ", ".join(f"{k}: {v}" for k, v in row.items())
                all_answers.append(f"[{row_str}]")
            answer = " | ".join(all_answers)  
            return f"Answer: {answer}"
        else:
            return "No data found for the provided ID."
            
    except Exception as e:
        return f"Error executing SQL:\n{sql_query}\n\nError: {str(e)}"
    finally:
        conn.close()


class ChatbotView(APIView):
    def post(self,request):
        try:
            serializer=ChatbotSerializer(data=request.data)
            if serializer.is_valid():
                personid=serializer.validated_data['personId']
                query=serializer.validated_data['query']
                status_code=serializer.validated_data['status']
                
                if status_code == '1':
                    combined_input = f"{query} | {personid}"
                    response = query_ssms_with_context_personal_details(combined_input,status_code)
                elif status_code == '2':
                    combined_input = f"{query}"
                    response = query_ssms_with_context_company_policy(combined_input,status_code)    

                print(" Response from query:", response)
                if response == False:
                    return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                # prompt = f"""You are a helpful and friendly HR chatbot assistant.

                #     Convert the following structured information into a clear, natural, and conversational sentence that directly answers the user's question. Do NOT include quotation marks or explain what you're doing — just return the direct chatbot-style answer.

                #     ### User Question:
                #     {query}

                #     ### Raw Data:
                #     {response}

                #     ### Chatbot Answer:"""
                if "I can't help you with that request" in response:
                    prompt = "Sorry, I can't help you with that, please contact HR."
                    return Response({"answer": prompt}, status=status.HTTP_200_OK)
                else:
                    prompt = (
                        f"Convert the following structured information into a human-readable format:\n\n"
                        f"Do not include any headings, explanations, or extra text. Just return the final sentence:\n\n"
                        f"Return ONLY the exact converted sentence. Do not add any prefixes like "
                        f"'Here is the answer', 'Converted information', or any extra text.\n\n"
                        f"{response}\n\n"
                        f"Make sure the result sounds like a natural sentence."
                        f"If the response contains 16 letters GUID,then you should refrain to return those GUIDs and its usage.Please return the final statement as:Expected Result Not Found"
                    )
                    human_readable_response = llm.invoke(prompt)
                
                    # responsecontent=str(human_readable_response.content)
                    return Response({"answer": human_readable_response.content}, status=status.HTTP_200_OK)

                

        except Exception as e:
            logger_function(filename,e,2)
            return Response({"status": "error", "message": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
            