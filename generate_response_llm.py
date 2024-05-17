from generate_sql_groq import generate_sql_groq, explain_result_groq, parse_sql_new
from run_sql import execute_query_df_json
import json

def generateResponseGroq(userPrompt, accountNumber):
    print(f"{userPrompt} \n\n account number is {accountNumber}") # for debugging only
    requestedPrompt = f"{userPrompt} whose account number is {accountNumber}"
    llmSql = generate_sql_groq(requestedPrompt)
    runSQl = parse_sql_new(llmSql)
    sqlResult = json.loads(execute_query_df_json(runSQl))
    print(sqlResult)
    res = explain_result_groq(sql_prompt=userPrompt, sql_result=sqlResult)
    # print(res)
    return {'data' : sqlResult, 'summary' : res}
    
# userPromt = "list all the policies"
# accountNumber = 10000
# d1 = generateResponseGroq(userPrompt=userPromt, accountNumber=accountNumber)
# print(d1)