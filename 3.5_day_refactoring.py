import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class simpleAgents:
    def __init__(self, system_prompt):
        self.client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
        self.memory = [{"role": "system", "content": system_prompt}]

        self.model = os.getenv('MODEL')

    def chat(self, user_message):
        print(f"User: {user_message}")
        self.memory.append({"role": "user", "content": user_message})

        try:
            response = self.client.chat.completions.create(
                messages=self.memory,
                model=self.model,
                temperature=0.7
            )

            aiResponse = response.choices[0].message.content
            print(f"Agent: {aiResponse}")

            self.memory.append({"role": "assistant", "content": aiResponse})

            return aiResponse
        except Exception as e:
            print('Getting error')
            return None

    def clear_memory(self):
        self.memory = [self.memory[0]]
        print("Agent memory clear")


if __name__ == '__main__':
    my_bot = simpleAgents("You are a helpful, concise assistant.")

    #test chat feature
    my_bot.chat("Hi My name is Arpit")
    my_bot.chat("Me aaj kal kya sikh raha hu")
    my_bot.chat("Mera naam kya hai")

    #menory clear    
    my_bot.clear_memory()
    my_bot.chat("Mera naam kya hai")