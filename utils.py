name = "C-3PO"

messages = [
    {
        "role": "system",
        "content": f"You are {name} a friendly, helpful personal assistant. You can query files, spreadsheets, APIs, and send emails. Be concise but thorough."
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