import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
groq_api_key = os.getenv('GROQ_API_KEY')

from groq import Groq

# define client for groq
client = Groq(
    api_key=groq_api_key
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="llama3-70b-8192",
)

print(chat_completion.choices[0].message.content)
