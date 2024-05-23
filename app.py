# restAPI for applications
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import datetime as dt
from run_sql import execute_query_df_json, get_data
import json as js
from generate_response_llm import generateResponseGroq, generateActionResponseGroq
from generate_response_llm_replicate import generateResponseReplicate,generateActionResponseReplicate
from generate_response_llm_gemini import generateResponseGemini, generateActionResponseGemini
from dotenv import load_dotenv, find_dotenv
import os

# load dotenv 
load_dotenv(find_dotenv())
genai_provider = os.getenv('GENAI_PROVIDER')

app = Flask(__name__)
cors = CORS(app=app)
app.config['CORS_HEADERS'] = 'Content-Type'


# for debugging only
@app.route('/', methods = ['GET', 'POST'])
@cross_origin()
def home():
    if(request.method == 'GET'):
        data = "Hello world"
        return jsonify({'data' : data})
    

# api for getting customer details
@app.route('/api/v1/sql/get-customer-details/<accountNumber>', methods = ['GET'])
def getAccountDetails(accountNumber):
    try:
        query = f"SELECT * FROM [dbo].[customer] WHERE account_number = {int(accountNumber)} "
        res = js.loads(execute_query_df_json(query))
        return res[0]
    except Exception as e:
        print(e)

# all policies of a particular customer
@app.route('/api/v1/sql/get-customer-policies/<accountNumber>', methods=['GET'])
def getCustomerPolicies(accountNumber):
    try:
        query = f"SELECT PolicyNumber, ExpirationDate, EffectiveDate,PolicyStatus FROM [dbo].[PolicyDetails] WHERE accountNumber = {int(accountNumber)};"
        res = js.loads(execute_query_df_json(query))
        return res
    except Exception as e:
        print(e)

# show more details of particular policy number
@app.route('/api/v1/sql/policy-details/<policyNumber>', methods = ['GET'])
def getPolicyDetails(policyNumber):
    if request.method == 'GET':
        query = f"SELECT * FROM [dbo].[PolicyDetails] WHERE PolicyNumber = '{str(policyNumber)}';"
        res = execute_query_df_json(query)
        return res

# llm genereates method

@app.route(rule='/api/v1/llm/prompt-results/<accountNumber>', methods=['POST'])
def generateResponse(accountNumber):
    if request.method == 'POST':
        data = request.get_json(force=True)
        userQuery = data['user_query']
        if(genai_provider == 'GROQ'):
            return generateResponseGroq(userPrompt=userQuery, accountNumber=accountNumber)
        if(genai_provider == 'REPLICATE'):
            return generateResponseReplicate(userPrompt=userQuery, accountNumber=accountNumber)
        if(genai_provider == 'GEMINI'):
            return generateResponseGemini(userPrompt=userQuery, accountNumber=accountNumber)
    else:
        return "Please use POST method"
    

@app.route('/api/v1/llm/enhance-result/<accountNumber>', methods=['POST'])
def generateActionResponse(accountNumber):
    if request.method == 'POST':
        data = request.get_json(force=True)
        userQuery = data['user_query']
        if(genai_provider == 'GROQ'):
            # print("groq") #for debugging Only
            return generateActionResponseGroq(userPrompt=userQuery, accountNumber=accountNumber)
        if(genai_provider == 'REPLICATE'):
            # print("rep") # for debugging only
            return generateActionResponseReplicate(userPrompt=userQuery, accountNumber=accountNumber)
        if(genai_provider == 'GEMINI'):
                # print("gem") # for debugging only
            return generateActionResponseGemini(userPrompt=userQuery, accountNumber=accountNumber)
    else:
        return "Please use POST method"
    

@app.route('/api/v1/sql/<policyNumber>/<accountNumber>/coverage-details', methods=['GET'])
def generateCoverageDetails(policyNumber, accountNumber):
    if request.method == 'GET':
        query = f"SELECT [c].[coverage_id], [c].[policy_id], [ct].[description] AS [coverage_type], [c].[limit], [c].[deductible] FROM [dbo].[Coverages] [c] INNER JOIN [dbo].[PolicyDetails] [pd] ON [c].[policy_id] = [pd].[PolicyID] INNER JOIN [dbo].[Customer] [cust] ON [pd].[AccountNumber] = [cust].[account_number] INNER JOIN [dbo].[Coverage_Types] [ct] ON [c].[coverage_type_id] = [ct].[coverage_type_id] WHERE [pd].[PolicyNumber] = '{policyNumber}' AND [cust].[account_number] = {accountNumber};"
        # print(query) # for debugging only
        data = js.loads(execute_query_df_json(query))
        return data
    else:
        return jsonify({'Error' : "Method Not Allowed"})
        

@app.route('/api/v1/sql/<policyNumber>/<accountNumber>/premium-amount', methods=['GET'])
def getPremiumAmount(accountNumber, policyNumber):
    if(request.method == 'GET'):
        query = f"SELECT [PremiumBalance] FROM [dbo].[PolicyDetails] AS p WHERE PolicyNumber = '{policyNumber}' AND accountNumber = {accountNumber};"
        data = js.loads(execute_query_df_json(query))
        return data[0]
    else:
        return jsonify({'Error' : "Method Not Allowed"})
        
@app.route('/api/v1/sql/policy-document/<accountNumber>/<policyNumber>', methods=['GET'])
def getPolicyDocumnets(policyNumber, accountNumber):
    if(request.method == 'GET'):
        query = f"SELECT [p].[DocumentLink] FROM [dbo].[PolicyDocuments] as [p] INNER JOIN [dbo].[PolicyDetails] AS [pd] ON [p].[PolicyID] = [pd].[PolicyID] INNER JOIN [dbo].[Customer] AS [c] ON [c].[account_number] = [pd].[AccountNumber] WHERE [pd].[PolicyNumber] = '{policyNumber}' AND [c].[account_number] = '{accountNumber}';"
        data = js.loads(get_data(query))
        return data[0]




if __name__ == '__main__':
    app.run(debug=True)