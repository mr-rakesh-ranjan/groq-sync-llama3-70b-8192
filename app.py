from generate_response_2_llm import generate_sql_2_groq, parse_sql_updated, explain_result
from run_sql import execute_query_df_json



# user question 
# user_qestion = "Show me the Claims with more than 10000 Total expenses"
user_question = "List all policies for Account number=10000 and their effective dates"

llm_response = generate_sql_2_groq(user_question=user_question)
print(llm_response)


generated_SQL = parse_sql_updated(llm_response)
# print(generated_SQL)

data = execute_query_df_json(generated_SQL)
print(data)

res = explain_result(sql_prompt=user_question, sql_result=data)
print(res)
