import os
from dotenv import load_dotenv
from groq import Groq

#setup
load_dotenv()
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

chat_message=[
    {
        "role": "system",
        "content": "You are a 5-year-old child. You answer questions correctly, but you always make a funny taunt about how simple the question is."
    },{
        "role": "user",
        "content": "Earth se Moon ka distance kitna hai?"
    }
]

print('AI is thinking')

response = client.chat.completions.create(
    messages=chat_message,
    model="llama-3.1-8b-instant"
)

print('AI Response is: ')
aiResponse = response.choices[0].message.content
print(aiResponse)