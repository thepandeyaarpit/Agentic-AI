import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def get_weather(city):
    print(f"\n[SYSTEM] Executing weather tool for: {city}...")
    if city.lower() == "surat":
        return "25C mast mausam hai"
    elif city.lower() == "dehradun":
        return "bahut thanda hai bhai"
    return "thik thak hai"


def calculate_math(expression):
    print(f"\n[SYSTEM] Executing math tool for: {expression}...")
    try:
        # result =  eval(expression)
        # return eval(result)
        return str(eval(expression))
    except Exception as e:
        return "Calculation error."
    

tools_list = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a specific city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Name of the city"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_math",
            "description": "Evaluate a mathematical expression (addition, multiplication, etc.).",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "The math expression, e.g., '25*40' or '100/4'"}
                },
                "required": ["expression"]
            }
        }
    }
]


# we are handling single and multiple both expression here

# user_prompt = "Surat ka weather kaisa chal raha hai aaj kal?"
# user_prompt = "Agar ek developer ki salary 85000 hai, toh uski 12 mahine ki total salary kitni hui?"
user_prompt = "Surat aur Dehradun dono ka weather batao, aur 1500 ko 12 se multiply karke result bhi batao."
chat_messages = [
    {"role": "system", "content": "You are a smart assistant. Use the appropriate tool to answer the user's question."},
    {"role": "user", "content": user_prompt}
]

response = client.chat.completions.create(
    messages=chat_messages,
    model=os.getenv('MODEL'),
    tools=tools_list,
    tool_choice="auto"
)

aiResponse = response.choices[0].message
chat_messages.append(aiResponse)

if aiResponse.tool_calls:
    print(f"AI Decision: Mujhe ek sath {len(aiResponse.tool_calls)} tools chalane honge!\n")
    for tool_call in aiResponse.tool_calls:
        func_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        print(f"AI Decision: Mujhe '{func_name}' tool use karna chahiye.")

        if func_name == "get_weather":
            result = get_weather(args.get('city'))
            print(f"[SYSTEM] Result: {result}")
        elif func_name == "calculate_math":
            result = calculate_math(args.get('expression'))
            print(f"[SYSTEM] Result: {result}")

        print(f" Tool '{func_name}' completed. Result: {result}")
        
        # Har result ko separately history me add karna zaroori hai
        chat_messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": func_name,
            "content": result
        })

else:
    print('-'*50)
    print("\n🤖 AI Answer (Bina tool ke):", aiResponse.content)
    print('-'*50)