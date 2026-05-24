from groq import Groq
import os

class GroqService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def get_reply(self, messages):
        response = self.client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages
        )

        return response.choices[0].message.content