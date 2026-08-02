import os
import json
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

load_dotenv()
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

class RouteDecision(BaseModel):
    category: str

def classify_intent(user_text):
    print("User ka intent samajh rahe hain...")

    router_prompt = f"""
    You are a classification router. Classify the user's text into one of these exact categories:
    - greeting
    - weather
    - math
    - unknown
    
    Respond ONLY with valid JSON in this format:
    {{
    "category": "<category>"
    }}

    User Text: "{user_text}"
    """

    response = client.chat.completions.create(
        messages = [
            {
                "role": "user", "content": router_prompt
            }
        ],
        model=os.getenv('MODEL'),
        response_format={"type": "json_object"},
        temperature=0.0
    )

    aiResponse = response.choices[0].message.content

    decision = RouteDecision.model_validate_json(aiResponse)
    return decision.category

user_input = "Hi there! Mera naam Arpit hai."
# user_input = "Surat me aaj barish hogi kya?"
# user_input = "2500 ka 15 percent kitna hoga?"

category = classify_intent(user_input)
print("Category is", category)

if category == "greeting":
    print("Agent: Hello! Main ek AI assistant hu. Main weather check kar sakta hu aur math solve kar sakta hu. Boliye kya madat karu?")
    
elif category == "weather":
    print("Triggering the Weather Workflow... (Yahan weather code chalega)")
    
elif category == "math":
    print("Triggering the Math Workflow... (Yahan calculator tool chalega)")
    
else:
    print("I am not trained to handle this request yet.")