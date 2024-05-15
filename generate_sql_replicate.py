import replicate # type: ignore
from dotenv import load_dotenv # type: ignore
from insurance_sql_prompt import sql_prompt
from pathlib import Path
import os

# load .env and replicate token
env_path = Path('.', '.env')
load_dotenv(dotenv_path=env_path)
replicate_token = os.getenv('REPLICATE_API_TOKEN')
print(replicate_token)

# configure  the replicate with its token
replicate = replicate.Client(api_token=replicate_token)

# for debugging only
user_prompt = "List all policies for Account number=10000 and their effective dates"

def generate_SQL_2_replicate(user_prompt) -> str:
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

# print(generate_SQL_2_replicate(user_prompt=user_prompt))

import pandas as pd
import json

def explain_result(sql_prompt, sql_result):
    user_prompt = f"""Summarize the results from the SQL query in less than or up to four sentences. 
    The result is an output from the following query: {sql_prompt}.
    Result: {sql_result}. 
    In the response, do not mention database-related words like SQL, rows, timestamps, etc."""

    response = replicate.run(
        "meta/meta-llama-3-70b-instruct",
        input=user_prompt
    )
    explanation = response.text
    
    result_summary = explanation
    result_list = None

    if "list" in sql_prompt.lower():
        result_list = sql_result.to_json(orient='records')
        
    print(explanation)
    return result_summary, result_list  
