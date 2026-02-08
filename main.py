from weather import get_current_weather
from history import save_chat_history, load_chat_history
from utils import name, messages, tools
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

try:
    history = load_chat_history()
    if history and history[0]["role"] == "system":
        messages = history
except FileNotFoundError:
    pass
except json.JSONDecodeError:
    print("Corrupt history file - starting fresh.")

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
            messages.append(choice.message.model_dump())
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
        messages.append({
            "role": "assistant",
            "content": output
        })
    except Exception as e:
        output = f"Oops, something went wrong: {e}. Try again?"
        print(output)

    save_chat_history(messages)