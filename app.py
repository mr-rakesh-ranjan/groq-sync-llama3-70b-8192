# restAPI for applications
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import datetime as dt
from run_sql import execute_query_df_json
import json as js
from generate_response_llm import generateResponseGroq


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
@cross_origin()
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

# pending
# @app.route('/api/v1/get-policy-details/<accountNumber>/<policyNumber>', methods = ['GET'])
@app.route('/api/v1/sql/get-policy-details')
@cross_origin
def getPolicyDetails(self):
    if request.method == 'GET':
        # query = f"SELECT * FROM [dbo].[PolicyDetails] WHERE PolicyNumber = {str(policyNumber)} and AccountNumber = {int(accountNumber)};"
        query = "SELECT * FROM [dbo].[PolicyDetails] WHERE PolicyNumber = 'mdy-3402747' and AccountNumber = 10001; "
        res = execute_query_df_json(query)
        return res

# llm genereates method

# @app.route('/api/v1/llm/prompt-results/<accountNumber>', methods = ['GET', 'POST'])
# @app.route("/api/v1/llm/prompt-results/<accountNumber>", methods=['POST'])
# @cross_origin
# def generateResponse(accountNumber):
#     if request.method == 'POST':
#         data = request.get_json(force=True)
#         userQuery = data['user_query']
#         try:
#             return generateResponseGroq(userPrompt=userQuery, accountNumber=accountNumber)
#         except Exception as e:
#             print(e)
#     else:
#         return "Please use POST method"

@app.route(rule='/api/v1/llm/prompt-results/<accountNumber>', methods=['POST'])
def generateResponse(accountNumber):
    if request.method == 'POST':
        data = request.get_json(force=True)
        userQuery = data['user_query']
        return generateResponseGroq(userPrompt=userQuery, accountNumber=accountNumber)
    else:
        return "Please use POST method"


if __name__ == '__main__':
    app.run(debug=True)
    
    