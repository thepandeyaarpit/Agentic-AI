import os
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

load_dotenv()

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

class userProfile(BaseModel):
    name: str
    age: int
    profession: str

chat_messages = [
    {
        "role": "system",
        # Hum AI ko Pydantic ka schema ek sample format me bata rahe hain
        "content": 'You are a data extractor. Output strictly in JSON format matching this schema: {"name": "string", "age": "integer", "profession": "string"}.'
    },
    {
        "role": "user",
        "content": "Hi! I am Amit. I turned thirty four last month, and I am a Data Scientist."
    }
]

reponse = client.chat.completions.create(
    messages=chat_messages,
    model="llama-3.1-8b-instant",
    response_format={"type": "json_object"}
)

aiResponse = reponse.choices[0].message.content
print(aiResponse)
print('*'*50)

# pydentic use
try:
    user_data = userProfile.model_validate_json(aiResponse)
    print('Pydentic checking data')
    print(f"Name: {user_data.name}")

    print(f"Age is after years is: {user_data.age + 5}")
except Exception as e:
    print('Error', e)