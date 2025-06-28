def input_getter(prompt:str):
    return input(prompt)

def json_editor(items,file_name):
    import json
    import os
    
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