import json
import os
def input_getter(prompt:str):
    return input(prompt)

def json_editor(items,file_name):
    json_dir = os.path.join(os.path.dirname(__file__), 'userdata')
    os.makedirs(json_dir, exist_ok=True)
    json_path = os.path.join(json_dir, f'{file_name}.json')

    
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            try:
                holdings = json.load(f)
            except json.JSONDecodeError:
                holdings = []
    else:
        holdings = []

    holdings.append(items)
    with open(json_path, "w") as f:
        json.dump(holdings, f, indent=2)

def json_extractor(file_name, transaction_type):
    json_dir = os.path.join(os.path.dirname(__file__), 'userdata')
    json_path = os.path.join(json_dir, f'{file_name}.json')

    with open(json_path, "r") as file:
        data = json.load(file)

    names = []
    for item in data:
        if item["type"] == transaction_type:
            name = item["name"]
            if name not in names:
                names.append(name)

    return names
