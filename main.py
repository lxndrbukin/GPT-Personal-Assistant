from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

name = "C-3PO"

messages = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": f"""You are {name} a friendly, helpful personal assistant. 
                       You can query files, spreadsheets, APIs, and send emails. Be concise but thorough."""
            }
        ]
    }
]

if len(messages) > 20:
    messages = [messages[0]] + messages[-19:]

while True:
    prompt = input("You:\n")
    if not prompt:
        continue
    if prompt == "/bye":
        break

    messages.append({
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": prompt
            }
        ]
    })

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages[:20],
            max_tokens=300,
            temperature=0.8
        )
        output = response.choices[0].message.content
    except Exception as e:
        output = f"Oops, something went wrong: {e}. Try again?"

    messages.append({
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": output
            }
        ]
    })
    print(f"\n{name}:\n{output}\n")

