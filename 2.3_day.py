from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ.get('GRQ_API_KEY'))

chat_messages = [
    {
        "role": "user",
        "content": "Explain Quantum Physics to a 5-year-old child in exactly 2 sentences."
    }
]

respone = client.chat.completions.create(
    messages=chat_messages,
    model="llama-3.1-8b-instant",

    # 1. Temperature (0.0 = ekdum strict/boring, 1.0 = creative/mazedar)
    # Experiment: Isko 0.0, phir 1.0, phir 2.0 karke try karna
    temperature=2,

    # 2. Max Tokens (Sirf 50 tokens tak ka answer allow karenge)
    # Agar answer lamba hua, toh wo beech me hi cut jayega
    max_tokens=100,

    # 3. Top-P (Ek aur randomness control - mostly isko 1 rakhte hain agar Temp use kar rahe hain)
    top_p=1,
)

print("🤖 AI ka Jawab:")
aiResponse = respone.choices[0].message.content
print("\n" + "-" * 50)
print(f"Total Token Usage: {respone.usage.total_tokens}")
print(f"Total Prompt Tokens: {respone.usage.prompt_tokens}")
print(f"Total Completion Tokens: {respone.usage.completion_tokens}")
print(aiResponse)