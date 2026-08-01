from httpx import Response
import os
from dotenv import load_dotenv
from groq import Groq

# load_dotenv = get data form .env file
load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

print("groq api key is loaded successfully")

response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "I am learning Agentic AI. Just say 'Setup successful, you are ready to code!' in a very exciting way."
        }
    ],
    model="llama-3.1-8b-instant"
)

print("AI Response is: ")
print(response.choices[0].message.content)
