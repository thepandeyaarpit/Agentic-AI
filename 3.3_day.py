import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def get_employee_salary(emp_id):
    if not isinstance(emp_id, int):
        return ValueError('emp_id must be an integer')
    if emp_id == 101:
        return "Employee salary is $85000"
    return "Employee not found"

tools_list = [
    {
        "type": "function",
        "function": {
            "name": "get_employee_salary",
            "description": "Get the salary of an employee using their ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    # AI ko bataya hai ki integer chahiye, par LLMs kabhi-kabhi text bhej dete hain
                    "emp_id": {"type": "integer", "description": "The Employee ID number"}
                },
                "required": ["emp_id"]
            }
        }
    }
]

chat_messages = [
    {"role": "system", "content": "You are a helpful assistant. Use the provided tools."},
    {"role": "user", "content": "Mujhe employee jiska ID 'one-zero-one' hai, uski salary batao."}
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
    for tool_call in aiResponse.tool_calls:
        func_name = tool_call.function.name
        arg = json.loads(tool_call.function.arguments)

        if func_name == 'get_employee_salary':
            try:
                result = get_employee_salary(arg.get('emp_id'))
            except ValueError as e:
                result = f"Error {e}"
                print("Error is {result}")

            chat_messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": func_name,
                "content": str(result)
            })

    # Here ai is cross check answer
    final_response = client.chat.completions.create(
        messages=chat_messages,
        model=os.getenv('MODEL')
    )

    print('FInal response is')
    print(final_response.choices[0].message.content)