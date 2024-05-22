import replicate 
from dotenv import load_dotenv 
from insurance_sql_prompt import sql_prompt
from pathlib import Path
import os

# load .env and replicate token
env_path = Path('.', '.env')
load_dotenv(dotenv_path=env_path)
replicate_token = os.getenv('REPLICATE_API_TOKEN')
# print(replicate_token) #for debugging only

# configure  the replicate with its token
replicate = replicate.Client(api_token=replicate_token)

# for debugging only
user_prompt = "List all policies for Account number=10000 and their effective dates"

def generate_SQL_replicate(user_prompt) -> str:
    input ={
        "prompt": f" {sql_prompt} Work through this problem step by step: \n\nQ: , {user_prompt} ?",
        "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    }
    temp : str = ""

    res = replicate.run(
        "meta/meta-llama-3-70b-instruct",
        input=input
    )
    
    temp = ''.join([str(element) for element in res])
    # print(temp)
    return temp

# testing for this function is remaining due to the free trails is expired.
def explain_result_replicate(sql_prompt, sql_result):
    user_prompt = f"""Summarize the results from the SQL query in less than or up to four sentences. 
    The result is an output from the following query: {sql_prompt}.
    Result: { sql_result}.
    In the response, do not mention database-related words like SQL, rows, timestamps, etc."""
    # print(user_prompt)
    input ={
        "prompt": f" {sql_prompt} Work through this problem step by step: \n\nQ: , {user_prompt} ?",
        "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    }
    response = replicate.run(
        "meta/meta-llama-3-70b-instruct",
        input=input
    )

    summary = ''
    summary = ''.join([str(element) for element in response])
    # print(summary) #for debugging only
    return summary
    

# # for debugging purpose
# from run_sql import execute_query_df_json
# from generate_sql_groq import parse_sql_new


# sqlQuery = generate_SQL_replicate(user_prompt='list all my policies of account number is 10008')
# rnableSQL = parse_sql_new(sqlQuery)
# sqlData = execute_query_df_json(rnableSQL)

# summ  = explain_result_replicate(sql_prompt=rnableSQL, sql_result=sqlData)
# print(summ)

