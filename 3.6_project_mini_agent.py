import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_weather(city):
    if city.lower() == 'surat':
        return "surat ka temprature 25 hai"
    elif city.lower() == "dehradun":
        return "dehradun ka temprature 20 hai"
    return "city not found"

def calculate_math(expression):
    try:
        return str(eval(expression))
    except:
        return "invalid expression"

tools_list = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a specific city.",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_math",
            "description": "Evaluate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"]
            }
        }
    }
]

class MiniAssistent:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
        self.model = os.getenv('MODEL')

        self.memory = [{
            "role": "system", 
            "content": "You are a smart, helpful assistant. You have access to weather and math tools. Use them only when necessary. Be concise."
        }]

    def chat(self, user_text):
        self.memory.append({
            "role": "user",
            "content": user_text
        })

        response = self.client.chat.completions.create(
            messages=self.memory,
            model=self.model,
            tools=tools_list,
            tool_choice='auto'
        )

        aiResponse = response.choices[0].message

        self.memory.append(aiResponse)

        if aiResponse.tool_calls:
            for tool_call in aiResponse.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                if func_name == 'get_weather':
                    result = get_weather(args.get('city'))
                elif func_name == 'calculate_math':
                    result = calculate_math(args.get('expression'))
                else:
                    result = "Tool not found"
                    
                self.memory.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": func_name,
                    "content": result
                })

            finalResponse = self.client.chat.completions.create(
                messages = self.memory,
                model=self.model
            )

            finalText = finalResponse.choices[0].message.content

            self.memory.append({
                "role": "assistant",
                "content": finalText
            })

            return finalText
        else:
            return aiResponse.content


if __name__ == '__main__':
    agent = MiniAssistent()

    print("="*50)
    print("Mini Assistant Ready! (Type 'quit' or 'exit' to stop)")
    print("="*50)

    while True:
        user_input = input ("You: ")
        if user_input.lower() in ['exit', 'bye']:
            print('Good Bye')
            break
        
        print("Assistant is typing...")
        reply = agent.chat(user_input)

        print(f"Assistant: {reply}")
        print("-" * 50)