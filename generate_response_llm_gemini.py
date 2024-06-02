from generate_sql_gemini import nl_sql_nl_gemini, explain_result_gemini, parse_triple_quotes
import json
from run_sql import get_data, execute_query_df_json
from datetime import datetime

def generateResponseGemini(userPrompt, accountNumber):
    requestedPrompt = f"{userPrompt} whose account number is {accountNumber}"
    llmSql = nl_sql_nl_gemini(requestedPrompt)
    runSQl = parse_triple_quotes(llmSql)
    sqlResult = json.loads(get_data(runSQl))
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

# def generateActionResponseGemini(userPrompt, accountNumber):
    start_time = datetime.now()
    
    requestedPrompt = f"{userPrompt} whose account number is {accountNumber}"
    
    
    llm_start_time = datetime.now()
    llmSql = nl_sql_nl_gemini(requestedPrompt)
    print(llmSql)
    llm_end_time = datetime.now()
    
    runSQl = parse_triple_quotes(llmSql)
    
    
    sql_exec_start_time = datetime.now()
    sqlResult = json.loads(get_data(runSQl))
    sql_exec_end_time = datetime.now()
    
    
    enhance_start_time = datetime.now()
    enhanceResult = enhance_policy_data(sqlQuery=runSQl, data=sqlResult, accountNumber=accountNumber)
    enhance_end_time = datetime.now()
    
    
    explain_start_time = datetime.now()
    summary = explain_result_gemini(sql_prompt=userPrompt, sql_result=sqlResult)
    explain_end_time = datetime.now()
    
    end_time = datetime.now()
    
    total_time_taken = end_time - start_time
    llm_time_taken = llm_end_time - llm_start_time
    sql_exec_time_taken = sql_exec_end_time - sql_exec_start_time
    enhance_time_taken = enhance_end_time - enhance_start_time
    explain_time_taken = explain_end_time - explain_start_time
    
    formatted_time = str(total_time_taken).split('.')[0]
    llm_time = str(llm_time_taken).split('.')[0]
    sql_exec_time = str(sql_exec_time_taken).split('.')[0]
    enhance_time = str(enhance_time_taken).split('.')[0]
    explain_time = str(explain_time_taken).split('.')[0]
    
    print(f"Total time taken: {formatted_time}")
    print(f"LLM time taken: {llm_time}")
    print(f"SQL execution time taken: {sql_exec_time}")
    print(f"Data enhancement time taken: {enhance_time}")
    print(f"Explanation time taken: {explain_time}")
    
    return {
        'data': enhanceResult,
        'summary': summary,
    }

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
			'url': f'/api/v1/sql/{policyNumber}/{accountNumber}/coverage-details'
		}
    ]
    return actions

