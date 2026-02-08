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
            "description": "Fetch current weather for a city. Use for ANY weather query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name, e.g., 'Madrid' or 'Barcelona, ES'."
                    }
                },
                "required": []
            }
        }
    }
]

while True:
    if len(messages) > 20:
        messages = [messages[0]] + messages[-19:]

    prompt = input("You:\n")
    if not prompt:
        continue
    if prompt == "/bye":
        break

    messages.append({
        "role": "user",
        "content": prompt
    })

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=300,
            temperature=0.9,
            stream=False
        )
        choice = response.choices[0]
        if choice.message.tool_calls:
            messages.append(choice.message)
            for tool_call in choice.message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                if function_name == "get_current_weather":
                    result = get_current_weather(**function_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": str(result)
                })
        stream_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.9,
            stream=True
        )
        output = ""
        print(f"\n{name}:\n", end="", flush=True)
        for chunk in stream_response:
            if chunk.choices[0].delta.content is not None:
                text = chunk.choices[0].delta.content
                print(text, end="", flush=True)
                output += text
        print("\n")

    except Exception as e:
        output = f"Oops, something went wrong: {e}. Try again?"
        print(output)