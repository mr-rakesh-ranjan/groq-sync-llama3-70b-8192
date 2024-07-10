# restAPI for applications
from flask import Flask, jsonify, request, session
from flask_cors import CORS, cross_origin
# from flask_api import status 
import datetime as dt
from email_otp import sendEmailVerificationRequest_smtp2go
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
secret_key = os.getenv('SECRET_KEY')

app = Flask(__name__)
cors = CORS(app=app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MAIL_USERNAME'] = 'insurance.chat'
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = secret_key


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
        data = js.loads(execute_query_df_json(query))
        return data[0]

# Apis for webhooks 
@app.route('/api/v2/account-details', methods=['POST'])
def accountDetails():
    if request.method =='POST':
        data = request.get_json(force=True, silent=True)
        print(data) #for  debugging 
        account_number = data['account_number']
        query = f"SELECT * FROM [dbo].[customer] WHERE account_number = {int(account_number)}"
        db_data = js.loads(get_data(query))
        return db_data[0]['customer_name']

@app.route('/loadchat/<account_number>/<session_id>', methods=['GET'])
def accounctChatLoad(account_number, session_id):
    if request.method == 'GET':
        query = f" SELECT[account_number],[session_id],[chat_time],[system_or_user],[chat_message] FROM [dbo].[chat_messages] WHERE account_number = {account_number} and session_id= '{session_id}' ORDER by chat_time ASC"
        result = js.loads(execute_query_df_json(query))
        return result
    
# Email verification System
@app.route('/api/v1/email-verification/<account_number>/<email>', methods=['POST'])
def emailVerification(account_number,email):
    if request.method == 'POST':
        query = f"SELECT * FROM [dbo].[customer] WHERE [customer_email] = '{email}' AND [account_number] = '{account_number}'"
        db_data = js.loads(execute_query_df_json(query))
        if db_data:
            receiver_email = db_data[0]['customer_email']
            # print(receiver_email) #for debuggiing only
            custom_message = f"Hello {db_data[0]['customer_name']}...  \n\nWelcome to the Insurence NLQ..."
            from email_otp import sendEmailVerificationRequest
            # current_otp = sendEmailVerificationRequest(receiver="rakesh_rk@pursuitsoftware.biz",message=custom_message)
            current_otp = sendEmailVerificationRequest(receiver=receiver_email, message=custom_message)
            session['current_otp'] = current_otp
            print(f"Otp saved in session : {session['current_otp']}")
            return jsonify({'status' : 'SUCCESS', 'message' : f'otp is {current_otp}'}), 200
        else:
            return jsonify({'status' : 'NOT FOUND', 'message' : 'Email does not exist'}), 404
    
@app.route('/api/v1/validate-otp', methods=['POST'])
def validate_otp():
    if request.method == 'POST':
        data = request.get_json(force=True, silent=True)
        print(data) #for  debugging
        user_otp = data['otp']
        if session:
            if int(user_otp) == int(session['current_otp']):
                return jsonify({'status' : 'SUCCESS', 'message' : 'Email verified successfully'}), 200
            else:
                return jsonify({'status' : 'Bad Request', 'message' : 'Email verification failed'}), 400


if __name__ == '__main__':
    app.run(debug=True, port=9900)