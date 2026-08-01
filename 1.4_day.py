import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

print('ready to start')


chat_message=[
    {
        "role": "system",
        "content": "You are a helpful assistant. You categorize words into 'Positive', 'Negative', or 'Neutral'. Only output the category name, nothing else"
    },
    # Example 1
    {"role": "user", "content": "Beautiful"},
    {"role": "assistant", "content": "Positive"},
    
    # Example 2
    {"role": "user", "content": "Terrible"},
    {"role": "assistant", "content": "Negative"},
    
    # Example 3
    {"role": "user", "content": "Table"},
    {"role": "assistant", "content": "Neutral"},
    
    # Hamara actual sawal
    {"role": "user", "content": "Frustrated"}
]

respone = client.chat.completions.create(
    messages=chat_message,
    model="llama-3.1-8b-instant"
)

print('AI response is: ')
print(respone.choices[0].message.content)