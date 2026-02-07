from weather import get_current_weather
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

name = "C-3PO"

messages = [
    {
        "role": "system",
        "content": f"""You are {name} a friendly, helpful personal assistant. 
                    You can query files, spreadsheets, APIs, and send emails. Be concise but thorough."""
    }
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get current weather for a city",
            "properties": {
                "city": {"type": "string", "description": "City name (optional). Extract from user message or conversation context, even follow-ups like 'and in X?' or 'what about Y?'."}
            },
            "required": []
        }
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
            tools=tools,
            tool_choice="auto",
            max_tokens=300,
            temperature=0.8
        )
        choice = response.choices[0]
        if choice.message.tool_calls:
            tool_call = choice.message.tool_calls[0]
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            if function_name == "get_current_weather":
                result = get_current_weather(**function_args)
            messages.append(choice.message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": result
            })
            second_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            output = second_response.choices[0].message.content
        else:
            output = choice.message.content
    except Exception as e:
        output = f"Oops, something went wrong: {e}. Try again?"

    messages.append({
        "role": "assistant",
        "content": output
    })
    print(f"\n{name}:\n{output}\n")

