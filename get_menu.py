# Creates a new list for the meal options
options = []

def list_to_dict(meal_data: list) -> dict:
    # Converts inputted list of meal details into dictionary which represents the meal's data, and then returns this dictionary
    return {
        "name": meal_data[0],
        "sell_for": float(meal_data[1]),
        "cost_to_make": float(meal_data[2]),
        "cook_time": float(meal_data[3]),
        "cook_time_stdev": float(meal_data[4])
    }

while True:
    # Takes in menu details as input separated by ","
    meal_data = input().split(",")

    # While loop will end and inputs will stop once "." is inputted
    if meal_data == ["."]:
        break

    # Adds inputted menu details to the list using list_to_dict(), converting numeric data types to float
    options.append(list_to_dict(meal_data))

# Default menu will be input into options if no meal data was input
if options == []:
    # Default menu's meals' data
    default_menu = [
        "Budda Bowl (vg),25,20,10,3",
        "Eye Fillet Steak,55,25,7,1",
        "Spaghetti Bolognese,30,22,40,5",
        "Pad Thai (seafood),22,17,30,1"
    ]

    # Adds default menu details to the list using list_to_dict(), converting numeric data types to float
    for i in default_menu:
        options.append(list_to_dict(i.split(",")))

# For loop prints the menu meal by meal
for i in range(len(options)):
    print(
        str(i + 1) + ".",
        "Name:" + options[i]["name"],
        "Sells:$" + str(options[i]["sell_for"]),
        "Costs:$" + str(options[i]["cost_to_make"]),
        "Takes:" + str(options[i]["cook_time"]), "mins"
    )
#python get_menu.py
#python test_get_menu.py
