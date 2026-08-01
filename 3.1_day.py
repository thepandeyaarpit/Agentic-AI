import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def get_weather(city):
    print(f"\n[SYSTEM] Executing Python function for city: {city}...")
    if city.lower() == "surat":
        return "30°C, Humid aur thodi barish ke chances hain."
    elif city.lower() == "delhi":
        return "40°C, Bohot garmi hai."
    return "25°C, Mausam saaf hai."


tools_list = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a given city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Name of the city"}
                },
                "required": ["city"]
            }
        }
    }
]

chat_messages = [
    {"role": "system", "content": "You are a helpful assistant. Use provided tools if needed. If not, answer directly."},
    {"role": "user", "content": "Surat ka mausam kaisa hai?"}
]

response = client.chat.completions.create(
    messages=chat_messages,
    model="llama-3.1-8b-instant",
    tools=tools_list,
    tool_choice="auto"
)

aiResponse = response.choices[0].message

chat_messages.append(aiResponse)

if aiResponse.tool_calls:
    for tool_call in aiResponse.tool_calls:
        func_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        if func_name == 'get_weather':
            function_result = get_weather(args.get("city"))
            print(f"[SYSTEM] Result from function: {function_result}\n")

            chat_messages.append({
                "role": "tool",
                "content": function_result,
                "tool_call_id": tool_call.id,
                "name": func_name
            })
    
    print("2. Data AI ko bhej diya, final answer ban raha hai...\n")

    final_response = client.chat.completions.create(
        messages=chat_messages,
        model="llama-3.1-8b-instant",
    )

    print("Final AI Answer:")
    print(final_response.choices[0].message.content)

else:
    print("AI Answer:", aiResponse.content)