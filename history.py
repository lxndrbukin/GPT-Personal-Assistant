import json

def save_chat_history(messages=[]):
    with open("chat_history.json", "w") as history:
        json.dump(messages, history, indent=4)

def load_chat_history():
    with open("chat_history.json", "r") as json_history:
        return json.load(json_history)
