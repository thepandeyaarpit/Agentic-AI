
import os
from dotenv import load_dotenv
from groq import Groq


# load environment variable
load_dotenv()

# setup the groq client
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))


# 2. Chat history array banayein (System prompt ke sath initialize karein)
# Aap yahan system prompt ko apne hisaab se change kar sakte hain
chat_history = [
    {"role": "system", "content": "You are a witty, sarcastic coding assistant. Keep your answers short and funny."}
]

print("🤖 Chatbot Ready! (Type 'quit' or 'exit' to stop)\n")
print("-" * 50)

while True:
    user_input = input("Aap: ")

    if(user_input.lower() in ['quit', 'exit']):
        print("Chatbot band ho raha hai. See you in Week 2!")
        break
    chat_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        messages=chat_history,
        model="llama-3.1-8b-instant",
    )

    ai_response = response.choices[0].message.content
    print("AI: ", ai_response)

    chat_history.append({"role": "assistant", "content": ai_response})