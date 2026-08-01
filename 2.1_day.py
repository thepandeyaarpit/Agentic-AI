import os
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

print('AI start-----')

chat_messages = [
    {
        "role": "system",
        # RULE 1: System prompt me clearly likhna padta hai ki JSON format me answer do
        "content": "You are a data extractor. You must output only in valid JSON format. Extract name, age, and profession from the user's text."
    },
    {
        "role": "user",
        "content": "Hi there! I am Amit. I recently turned 32 last month, and I have been working as a Data Scientist for the last 5 years."
    }
]

response = client.chat.completions.create(
    messages=chat_messages,
    model="llama-3.1-8b-instant", 
    response_format={"type": "json_object"}
)

aiResponse = response.choices[0].message.content
print(aiResponse)

print("--------------------------------------------------")
parsed_data = json.loads(aiResponse)
print(f"Name: {parsed_data.get('name')}")
print(f"Age: {parsed_data.get('age')}")
print(f"Profession: {parsed_data.get('profession')}")
