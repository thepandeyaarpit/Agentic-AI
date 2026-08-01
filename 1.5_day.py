import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
modelUse = Groq(api_key=os.environ.get('MODEL'))


print('ready to start')

# Humara Puzzle prompt
# Notice the magic phrase at the end!
chat_messages=[
    {
        "role": "user",
        "content": "A snail is at the bottom of a 20-foot well. Each day, it climbs up 5 feet, but at night, it slips down 4 feet. How many days will it take for the snail to reach the top of the well? Let's think step by step."
    }
]

print('AI is thinking')

response = client.chat.completions.create(
    messages=chat_messages,
    model="llama-3.1-8b-instant", 
)

print('message content is: ')
print(response.choices[0].message.content)