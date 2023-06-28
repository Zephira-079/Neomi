import os

config_path = "./config.txt"

def get_config():
    key_collection = {}
    if os.path.exists(config_path):
        with open(config_path, "r") as cf:
            cf_items = cf.readlines()
            for item in cf_items:
                item = item.strip()
                if item:
                    key, value = item.split("=")
                    key_collection[key.strip()] = value.strip()
    else:
        return key_collection
        
    return key_collection

environment = get_config()
def neomi_key():
    return environment.get("neomi")