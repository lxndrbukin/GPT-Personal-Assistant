from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

messages = [
    {"role": "system", "content": "You are a friendly, helpful personal assistant. You can query files, spreadsheets, APIs, and send emails. Be concise but thorough."}
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    max_tokens=250
)

print(response)
