import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
print('Bot start')

client=Groq(api_key=os.environ.get('GROQ_API_KEY'))

chat_message=[
    {
        "role": "system",
        "content": ""
    }
]

while True:
    user_input = input('You: ')

    if user_input.lower() in ['exit','quit','bye','goodbye']:
        print('Okay: bye')
        break

    chat_message.append(
        {
            "role": "user",
            "content": user_input
        }
    )
    response = client.chat.completions.create(
        messages=chat_message,
        model="llama-3.1-8b-instant",
    )   
    
    mainResponse = response.choices[0].message.content
    print('Bot: ', mainResponse)
    
    chat_message.append({"role": "assistant", "content": mainResponse})