# import os
# from dotenv import load_dotenv, find_dotenv

# load_dotenv(find_dotenv())
# groq_api_key = os.getenv('GROQ_API_KEY')

# from groq import Groq

# # define client for groq
# client = Groq(
#     api_key=groq_api_key
# )

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Explain the importance of fast language models",
#         }
#     ],
#     model="llama3-70b-8192",
# )

# print(chat_completion.choices[0].message.content)


# restAPI for applications
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import datetime as dt

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
    
# import os
# from dotenv import load_dotenv, find_dotenv

# load_dotenv(find_dotenv())
# groq_api_key = os.getenv('GROQ_API_KEY')

# from groq import Groq

# # define client for groq
# client = Groq(
#     api_key=groq_api_key
# )

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Explain the importance of fast language models",
#         }
#     ],
#     model="llama3-70b-8192",
# )

# print(chat_completion.choices[0].message.content)

# import os
# from dotenv import load_dotenv, find_dotenv

# load_dotenv(find_dotenv())
# groq_api_key = os.getenv('GROQ_API_KEY')

# from groq import Groq

# # define client for groq
# client = Groq(
#     api_key=groq_api_key
# )

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Explain the importance of fast language models",
#         }
#     ],
#     model="llama3-70b-8192",
# )

# print(chat_completion.choices[0].message.content)
