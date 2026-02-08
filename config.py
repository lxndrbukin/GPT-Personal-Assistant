import json

CONFIG_FILE = "config.json"

def create_config(
        assistant_name="C-3PO",
        model="gpt-4o-mini",
        max_tokens=300,
        temperature=0.9,
        max_history_count=20,
        stream_delay=0.05
    ):
    return {
          "openai": {
            "model": f"{model}",
            "max_tokens": max_tokens,
            "temperature": temperature
          },
          "assistant": {
            "name": f"{assistant_name}"
          },
          "conversation": {
            "max_history_count": max_history_count
          },
          "ui": {
            "stream_delay": stream_delay
          }
    }

def save_config(config):
    with open(CONFIG_FILE, "w") as config_file:
        json.dump(config, config_file)