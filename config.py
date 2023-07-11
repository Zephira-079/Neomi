import os
import json

config_path = "./config.json"

def get_config():
    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            return json.load(file)
    return {}

environment = get_config()

def get(token_name):
    for token in environment.get("tokens", []):
        if token.get("name", "").strip() == token_name.strip():
            return token.get("value")

    return os.environ.get(token_name)
