from insurance_sql_prompt import sql_prompt
import google.generativeai as genai
import os
from dotenv import load_dotenv, find_dotenv
 
load_dotenv(find_dotenv())
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


def nl_sql_nl_gemini(user_prompt):
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)

    models = genai.GenerativeModel('gemini-pro')
    response = models.generate_content( f"{sql_prompt} \n\n Generate SQL for : {user_prompt}",

                                          generation_config=genai.types.GenerationConfig(temperature=0)
                                      )
    return response.text

def parse_triple_quotes(in_str):
  start = in_str.find("```sql") + len("```sql\n")  
  end = in_str.rfind("```") 
  out_str = in_str[start:end].strip()
  return out_str

def explain_result_gemini(sql_prompt, sql_result):
    user_prompt = f"""Summarize the results from the SQL query in less than or up to four sentences. 
    The result is an output from the following query: {sql_prompt}.
    Result: {sql_result}. 
    In the response, do not mention database-related words like SQL, rows, timestamps, etc."""

    models = genai.GenerativeModel('gemini-pro')
    response = models.generate_content(user_prompt)
    explanation = response.text
    return explanation 
