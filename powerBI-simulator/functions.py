import json
def get_stocks_from_json(file_path='list_of_stocks.json'):
    with open(file_path, 'r') as file:
        data = json.load(file)
    stocks_data = data.get("stocks", [])
    return stocks_data
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
def on_button_click(parameter):
    print(f"Button clicked with parameter: {parameter}")

if __name__ == "__main__":
    
    # a = get_stocks_from_json()
    # lens = [len(i) for i in a]
    # print(lens)
    # print(max(lens))
    buttons_data = ["Button 1", "Button 2", "Button 3"]
    button_functions = [
        lambda: on_button_click("Parameter 1"),
        lambda: on_button_click("Parameter 2"),
        lambda: on_button_click("Parameter 3")
    ]

    for button_data, button_function in zip(buttons_data, button_functions):
        print(button_data, button_function)