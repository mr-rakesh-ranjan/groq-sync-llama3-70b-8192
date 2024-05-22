from generate_sql_gemini import nl_sql_nl_gemini, explain_result_gemini, parse_triple_quotes
from run_sql import execute_query_df_json
import json

def generateResponseGemini(userPrompt, accountNumber):
    requestedPrompt = f"{userPrompt} whose account number is {accountNumber}"
    llmSql = nl_sql_nl_gemini(requestedPrompt)
    runSQl = parse_triple_quotes(llmSql)
    sqlResult = json.loads(execute_query_df_json(runSQl))
    res = explain_result_gemini(sql_prompt=userPrompt, sql_result=sqlResult)
    return {'data' : sqlResult, 'summary' : res}
    
def generateActionResponseGemini(userPrompt, accountNumber):
    requestedPrompt = f"{userPrompt} whose account number is {accountNumber}"
    llmSql = nl_sql_nl_gemini(requestedPrompt)
    runSQl = parse_triple_quotes(llmSql)
    sqlResult = json.loads(execute_query_df_json(runSQl))
    enhanceResult = enhance_policy_data(sqlQuery=runSQl, data=sqlResult, accountNumber=accountNumber)
    summary = explain_result_gemini(sql_prompt=userPrompt, sql_result=sqlResult)
    return {'data' : enhanceResult, 'summary': summary}

def enhance_policy_data(sqlQuery, data, accountNumber):
    if 'SELECT' in sqlQuery and 'PolicyDetails' in sqlQuery:
        for policy in data:
            if 'PolicyNumber' and 'PremiumBalance' in policy:
                policyNumber = policy['PolicyNumber']
                premiumBalance = policy['PremiumBalance']
                policy['actions'] = createDynamicActions(policyNumber=policyNumber,premiumBalance=premiumBalance, accountNumber=accountNumber )
            else:
                return data
    return data

def createDynamicActions(policyNumber, premiumBalance, accountNumber):
    actions = [
        {
			'label':'Pay',
			'url': f'https://zohosecurepay.com/checkout/45sm9zp-3rmtgxcc9el2bm/Invoice-Payment?amount={premiumBalance}',
		},
		{  
			'label':'Show more Details' ,
			'url': f'/api/v1/sql/policy-details/{policyNumber}'
		},
		{ 
			'label':'Show Coverage',
			'url': f'/api/v1/llm/{policyNumber}/{accountNumber}/coverage-details'
		}
    ]
    return actions

