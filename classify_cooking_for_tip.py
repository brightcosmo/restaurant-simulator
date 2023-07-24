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

# Takes the customer's choice and the meal's cooking time
choice_and_time = input().split(",")
choice = int(choice_and_time[0])
time_taken = float(choice_and_time[1])


def get_classification(time_taken: float, cook_time: float, cook_time_stdev: float) -> str:
    # Determines classification and tip for meal
    if time_taken < cook_time - 2 * cook_time_stdev:
        return "was very undercooked and cooking tip was -100%"
    elif time_taken >= cook_time - 2 * cook_time_stdev and time_taken <= cook_time - cook_time_stdev:
        return "was slightly undercooked and cooking tip was 0%"
    elif time_taken > cook_time - cook_time_stdev and time_taken < cook_time + cook_time_stdev:
        return "was well cooked and cooking tip was 10%"
    elif time_taken >= cook_time + cook_time_stdev and time_taken <= cook_time + 2 * cook_time_stdev:
        return "was slightly overcooked and cooking tip was 0%"
    else:
        return "was very overcooked and cooking tip was -100%"

# Prints meal classification with tip
print(options[choice - 1]["name"], get_classification(time_taken, options[choice - 1]["cook_time"], options[choice - 1]["cook_time_stdev"]))
