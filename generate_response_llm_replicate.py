from generate_sql_replicate import generate_SQL_replicate, explain_result_replicate
from generate_response_llm import parse_sql_new, enhance_policy_data
from run_sql import execute_query_df_json
import json


def generateResponseReplicate(userPrompt, accountNumber):
    print(f"{userPrompt} and its account number is {accountNumber}") # for debugging Only
    requestedPrompt = f"{userPrompt} whose account number is {accountNumber}"
    llmSql = generate_SQL_replicate(requestedPrompt)
    runnableSQl = parse_sql_new(llmSql)
    sqlResult = json.loads(execute_query_df_json(runnableSQl))
    print(sqlResult) # for debugging only
    res = explain_result_replicate(sql_prompt=userPrompt, sql_result=sqlResult)
    print(res) # for debugging only
    return {'data' : sqlResult, 'summary' : res}

def generateActionResponseGroq(userPrompt, accountNumber):
    # print("function call") # for debugging only
    # print(f"{userPrompt} \n\n account number is {accountNumber}") # for debugging only
    requestedPrompt = f"{userPrompt} whose account number is {accountNumber}"
    llmSql = generate_SQL_replicate(requestedPrompt)
    runSQl = parse_sql_new(llmSql)
    print(runSQl) # for debugging only
    sqlResult = json.loads(execute_query_df_json(runSQl))
    # print(type(sqlResult)) # for debugging only
    enhanceResult = enhance_policy_data(sqlQuery=runSQl, data=sqlResult, accountNumber=accountNumber)
    # print(enhanceResult) # for debugging only
    summary = explain_result_replicate(sql_prompt=userPrompt, sql_result=sqlResult)
    return {'data' : enhanceResult, 'summary': summary}


# for debugging purpose
# d1 = generateActionResponseGroq(userPrompt="list all my policies", accountNumber=10006)
# print(d1)