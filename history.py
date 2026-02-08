import json

def save_chat_history(messages=[]):
    with open("chat_history.json", "w") as history:
        json.dump(messages, history, indent=4)

def load_chat_history():
    with open("chat_history.json", "r") as json_history:
        return json.load(json_history)

def trim_history(messages, max_count=20):
    if len(messages) <= max_count:
        return messages

    system_message = messages[0]
    conversation = messages[1:]

    turns = find_complete_turns(conversation)

    def count_messages():
        count = 1
        for turn in turns:
            count += len(turn)
        return count

    while count_messages() > max_count:
        if turns:
            turns.pop(0)
        else:
            break

    result = [system_message]
    for turn in turns:
        result.extend(turn)

    return result

def find_complete_turns(messages):
    turns = []
    current_turn = []

    for msg in messages:
        current_turn.append(msg)

        if msg["role"] == "assistant" and "tool_calls" not in msg:
            turns.append(current_turn)
            current_turn = []

    if current_turn:
        turns.append(current_turn)

    return turns