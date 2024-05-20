from insurance_sql_prompt import sql_prompt
from groq import Groq
import os
from dotenv import load_dotenv, find_dotenv

# load dotenv 
load_dotenv(find_dotenv())
groq_api_key = os.getenv('GROQ_API_KEY')

# define client as Groq
client = Groq(
    api_key=groq_api_key
)


# define a text_to_sql function which takes in the system prompt and the user's question and outputs the LLM-generated Ms-SQL query. Note that since we are using Groq API's JSON mode to format our output, we must indicate our expected JSON output format in either the system or user prompt.
def generate_sql_groq(user_question):
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        # response_format = {"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": sql_prompt
            },
            {
                "role": "user",
                "content": user_question
            }
        ]
    )
    return completion.choices[0].message.content

def parse_sql_updated(gen_sql):
    # finding the position of '```' and removing the '```' and the newlines
    start = gen_sql.find("```") + len("```\n")
    # finding position of ending '```' and removing the '```'
    end = gen_sql.rfind("```")
    # apply strip method on input_string
    out_string = gen_sql[start+2:end].strip()
    # print(f"OUTPUT STRING {out_string}") # for debugging only
    return out_string

def parse_sql_new(gen_sql):
    if '```sql' in gen_sql:
        print("counter")
        # finding the position of '```' and removing the '```' and the newlines
        start = gen_sql.find("```sql") + len("```\n")
        # finding position of ending '```' and removing the '```'
        end = gen_sql.rfind("```")
        # apply strip method on input_string
        out_string = gen_sql[start+2:end].strip()
        # print(f"OUTPUT STRING {out_string}") # for debugging only
        return out_string
    else:
        print("reloader")
        # finding the position of '```' and removing the '```' and the newlines
        start = gen_sql.find("```") + len("```\n")
        # finding position of ending '```' and removing the '```'
        end = gen_sql.rfind("```")
        # apply strip method on input_string
        out_string = gen_sql[start:end].strip()
        # print(f"OUTPUT STRING {out_string}") # for debugging only
        return out_string

def explain_result_groq(sql_prompt, sql_result):
    user_prompt = f"""Summarize the results from the SQL query in less than or up to four sentences. 
    The result is an output from the following query: {sql_prompt}.
    Result: {sql_result}. 
    In the response, do not mention database-related words like SQL, rows, timestamps, etc."""

    completions = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": user_prompt,
        }
    ],
    model="llama3-70b-8192",
    )
    explanation = completions.choices[0].message.content
    
    # print(explanation) # for debugging only
    return explanation  
