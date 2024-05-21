# restAPI for applications
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import datetime as dt
from run_sql import execute_query_df_json
import json as js
from generate_response_llm import generateResponseGroq, generateActionResponseGroq


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
        return generateResponseGroq(userPrompt=userQuery, accountNumber=accountNumber)
    else:
        return "Please use POST method"
    

@app.route('/api/v1/llm/enhance-result/<accountNumber>', methods=['POST'])
def generateActionResponse(accountNumber):
    if request.method == 'POST':
        data = request.get_json(force=True)
        userQuery = data['user_query']
        return generateActionResponseGroq(userPrompt=userQuery, accountNumber=accountNumber)
    else:
        return "Please use POST method"
    

@app.route('/api/v1/llm/<policyNumber>/<accountNumber>/coverage-details', methods=['GET'])
def generateCoverageDetails(policyNumber, accountNumber):
    if request.method == 'GET':
        prompt = request.args['prompt']
        # print(prompt) # for debugging only
        requestedPrompt = f"{prompt} whose policy number is {policyNumber}"
        return generateActionResponseGroq(userPrompt=requestedPrompt, accountNumber=accountNumber)




if __name__ == '__main__':
    app.run(debug=True)
    
    