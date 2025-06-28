import uuid
from tools import input_getter,json_editor,json_extractor


def new_holding():
    import uuid
    
    type = int(input_getter("What would you like to add to your portfolio?\n1. Shares\n2. Crypto\n3. ETF\nInput: "))
    if type == 1:
        type_str = "shares"
    elif type == 2:
        type_str = "crypto"
    else:
        type_str = "ETF"
    transaction_id = f"buy-{type_str}-{str(uuid.uuid4())}"
    holding_name = input_getter(f"What is the ticker of the {type_str} you want to add (ex.Apple inc's ticker is AAPL)?\nInput: ").upper()
    holding_num = input_getter(f"How many units {holding_name} did you buy?\nInput: ")
    holding_date = input_getter(f"When did you purchase {holding_name}(format: DD/MM/YYYY)?\nInput: ")
    print(f"Hooray! You have added {holding_num} units of {holding_name} to your portfolio")


    holding = {
        "transaction_id": transaction_id,
        "type": type_str,
        "name": holding_name,
        "units": holding_num,
        "date": holding_date,
        "sell/buy": "buy"
    }
    json_editor(holding,"transactions")
    
    return holding

def del_holding():
    type_input = input_getter(
        "What would you like to sell from your portfolio?\n""1. Shares\n2. Crypto\n3. ETF\nInput: "
        )

    type_map = {
        "1": "shares",
        "2": "crypto",
        "3": "ETF"
    }

    type_str = type_map.get(type_input)
    transaction_id = f"sell-{type_str}-{uuid.uuid4()}"

    sellable_holdings = json_extractor("transactions", type_str)

    if not sellable_holdings:
        print(
            f"You have no {type_str} to sell in your portfolio."
            )
        return

    print(
        f"You can sell one of the following {type_str}:"
        )
    for item in sellable_holdings:
        print(item)

    holding_name = input_getter(
        f"What is the ticker of the {type_str} you want to sell (e.g., AAPL for Apple)?\nInput: "
    ).upper()

    holding_units = input_getter(
        f"How many units of {holding_name} would you like to sell?\nInput: "
        )
    holding_date = input_getter(
        f"When did you purchase {holding_name}? (format: DD/MM/YYYY)\nInput: "
    )

    print(
        f"{holding_units} units of {holding_name} marked as sold from your portfolio."
        )

    holding = {
        "transaction_id": transaction_id,
        "type": type_str,
        "name": holding_name,
        "units": holding_units,
        "date": holding_date,
        "sell/buy": "sell"
    }

    json_editor(holding, "transactions")

    return holding

    
del_holding()



