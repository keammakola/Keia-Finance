from tools import input_getter,json_editor


def new_holding():
    type = int(input_getter("What would you like to add to your portfolio?\n1. Shares\n2. Crypto\n3. ETF\nInput: "))
    if type == 1:
        type_str = "shares"
    elif type == 2:
        type_str = "crypto"
    else:
        type_str = "ETF"
    holding_name = input_getter(f"What is the ticker of the {type_str} you want to add (ex.Apple inc's ticker is AAPL)?\nInput: ").upper()
    holding_num = input_getter(f"How many units {holding_name} did you buy?\nInput: ")
    holding_date = input_getter(f"When did you purchase {holding_name}?\nInput: ")
    print(f"Hooray! You have added {holding_num} units of {holding_name} to your portfolio")

    
    holding = {
        "type": type_str,
        "name": holding_name,
        "units": holding_num,
        "date": holding_date
    }
    json_editor(holding,"holdings")
    
    return holding

    

new_holding()

