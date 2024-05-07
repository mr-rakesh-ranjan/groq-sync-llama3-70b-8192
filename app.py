from insurance_sql_prompt import sql_prompt
from generate_response_2_llm import text_to_sql
from groq import Groq
import os
from dotenv import load_dotenv, find_dotenv

# load dotenv 
load_dotenv(find_dotenv())
groq_api_key = os.getenv('GROQ_API_KEY')

# define clienty as Groq
client = Groq(
    api_key=groq_api_key
)


# user question 
# user_qestion = "Show me the Claims with more than 10000 Total expenses"
user_question = "List all policies for Account number=10000 and their effective dates"

llm_response = text_to_sql(client=client, system_prompt=sql_prompt, user_question=user_question)
print(llm_response)