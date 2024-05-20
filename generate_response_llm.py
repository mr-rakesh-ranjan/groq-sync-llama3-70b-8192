from generate_sql_groq import generate_sql_groq, explain_result_groq, parse_sql_new
from run_sql import execute_query_df_json
import json

def generateResponseGroq(userPrompt, accountNumber):
    print(f"{userPrompt} \n\n account number is {accountNumber}") # for debugging only
    requestedPrompt = f"{userPrompt} whose account number is {accountNumber}"
    llmSql = generate_sql_groq(requestedPrompt)
    runSQl = parse_sql_new(llmSql)
    sqlResult = json.loads(execute_query_df_json(runSQl))
    # print(sqlResult) # for debugging only
    res = explain_result_groq(sql_prompt=userPrompt, sql_result=sqlResult)
    # print(res) # for debugging only
    return {'data' : sqlResult, 'summary' : res}
    
def generateActionResponseGroq(userPrompt, accountNumber):
    # print("function call") # for debugging only
    # print(f"{userPrompt} \n\n account number is {accountNumber}") # for debugging only
    requestedPrompt = f"{userPrompt} whose account number is {accountNumber}"
    llmSql = generate_sql_groq(requestedPrompt)
    runSQl = parse_sql_new(llmSql)
    # print(type(runSQl)) # for debugging only
    sqlResult = json.loads(execute_query_df_json(runSQl))
    # print(type(sqlResult)) # for debugging only
    enhanceResult = enhance_policy_data(sqlQuery=runSQl, data=sqlResult)
    # print(enhanceResult) # for debugging only
    summary = explain_result_groq(sql_prompt=userPrompt, sql_result=sqlResult)
    return {'data' : enhanceResult, 'summary': summary}


def enhance_policy_data(sqlQuery, data):
    # print("enhance") # for debugging only
    # Check if the SQL query is selecting from [dbo].[PolicyDetails]
    # print(f'sample - {data}') # for debugging only
    if "SELECT" in sqlQuery and "[dbo].[PolicyDetails]" in sqlQuery:
        # Add the actions to each policy in the data list
        for policy in data:
            if 'PolicyNumber' in policy:
                policyNumber = policy['PolicyNumber']
                print(policyNumber)
                policy['actions'] = createDynamicActions(policyNumber=policyNumber)
            else:
                return data
    # Return the modified list of dictionaries
    return data

def createDynamicActions(policyNumber):
    actions = [
        {
            'label': 'Pay',
            'url': f'/insuranceapplication/policy/pay/{policyNumber}'
        },
        {
            'label': 'Show more Details',
            'url': f'api/v1/llm?prompt=show details of policy {policyNumber}'
        },
        {
            'label': 'Show Coverage',
            'url': f'/api/v1/sql/policy/coverage/{policyNumber}'
        }
    ]
    return actions


# testing for generate response :::
# userPromt = "list all the policies"
# accountNumber = 10001
# d1 = generateActionResponseGroq(userPrompt=userPromt, accountNumber=accountNumber)
# print(d1)

# testing for enhance_policy_data
# sqlQuery = 'SELECT [p].[PolicyNumber], [p].[TermNumber], [p].[EffectiveDate], [p].[ExpirationDate], [p].[AccountNumber] FROM [dbo].[PolicyDetails] [p] INNER JOIN [dbo].[Customer] [c] ON [p].[AccountNumber] = [c].[account_number] WHERE [c].[account_number] = 10001;'
# data = [{'PolicyNumber': 'DNf-0052546', 'TermNumber': '3', 'EffectiveDate': '2023-10-10T00:00:00.000', 'ExpirationDate': '2024-10-09T00:00:00.000', 'AccountNumber': '10001'}, {'PolicyNumber': 'oAd-1791934', 'TermNumber': '4', 'EffectiveDate': '2024-04-12T00:00:00.000', 'ExpirationDate': '2025-04-12T00:00:00.000', 'AccountNumber': '10001'}, {'PolicyNumber': 'hDw-2008648', 'TermNumber': '3', 'EffectiveDate': '2023-11-01T00:00:00.000', 'ExpirationDate': '2024-10-31T00:00:00.000', 
# 'AccountNumber': '10001'}]

# d1 = enhance_policy_data(sqlQuery=sqlQuery,data=data)
# print(type(d1))