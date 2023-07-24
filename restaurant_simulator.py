from random import random, gauss

# Default menu used in R1 and R2, unless different menu items are inputted
default_menu =[['Budda Bowl (vg)',25,20,10,3],
               ['Eye Fillet Steak',55,25,7,1],
               ['Spaghetti Bolognese',30,22,40,5],
               ['Pad Thai (seafood)',22,17,30,1]]

# R1 - Takes input from user for menu items
def get_meals_list_from_user():
    options = []

    # Takes in menu details as input separated by ","
    # While loop will end and inputs will stop once "." is inputted
    while True:
        meal_data = input().split(",")
        if meal_data == ["."]:
            # If statement - sets options to default menu if "." is inputted initially
            if options == []:
                options += default_menu
            break
        # Appends inputted meal data into options list
        options.append(meal_data)
    
    # Converts inputted menu details in options to dictionaries, converting numeric data types to float
    for i in range(len(options)):
        options[i] = {
            "name": options[i][0],
            "sell_for": float(options[i][1]),
            "cost_to_make": float(options[i][2]),
            "cook_time": float(options[i][3]),
            "cook_time_stdev": float(options[i][4])
        }

    # Returns the menu items
    return options


# R2 - Displays the menu as inputted in R1 to the user
def display_menu(options):
    # For loop to print each item in the list individually
    for i in range(len(options)):
        print(
            str(i + 1) + ".",
            "Name:" + options[i]["name"],
            "Sells:$" + str(options[i]["sell_for"]),
            "Costs:$" + str(options[i]["cost_to_make"]),
            "Takes:" + str(options[i]["cook_time"]), "mins"
        )


# R3 - Validating input by user
def validate_user_choice(options,user_input):
    # Checks if user input is a digit, and if the digit is valid for the menu
    # Then, checks through the whole list to see if there exists a meal matching the number inputted by the user
    if user_input.isdigit():
        number_meal = int(user_input)
        for i in range(len(options)):
            if i + 1 == number_meal:
                return True
        return False
    else:
        return False


# R5 - Classifies cooking time as undercooked, overcooked, or well cooked
# Compares actual cook time compares to average and stdev of cooking time, then returns classificiation
def classify_cook_time(average_cook_time, stdev_cook_time, actual_cook_time):
    if actual_cook_time < average_cook_time - 2 * stdev_cook_time:
        return "very undercooked"
    elif actual_cook_time >= average_cook_time - 2 * stdev_cook_time and actual_cook_time <= average_cook_time - stdev_cook_time:
        return "slightly undercooked"
    elif actual_cook_time > average_cook_time - stdev_cook_time and actual_cook_time < average_cook_time + stdev_cook_time:
        return "well cooked"
    elif actual_cook_time >= average_cook_time + stdev_cook_time and actual_cook_time <= average_cook_time + 2 * stdev_cook_time:
        return "slightly overcooked"
    else:
        return "very overcooked"


# R5 - Determines cooking tip based on classification
def get_cooking_tip(classification, base_tip):
    if classification == "very undercooked":
        return(-100)
    elif classification == "slightly undercooked":
        return(0)
    elif classification == "well cooked":
        return(base_tip)
    elif classification == "slightly overcooked":
        return(0)
    elif classification == "very overcooked":
        return(-100)


# R7 - Determines tip based on random comparison
# If random value is lower than tip chance, tip is positive
# If random value is higher than (1-chance), tip is negative
# Otherwise, tip is 0
def random_tip_compute(tip_chance, base_tip_value, random_comparison):
    if random_comparison < tip_chance:
        return base_tip_value
    elif random_comparison > 1 - tip_chance:
        return -base_tip_value
    else:
        return 0


# R8 - Displays menu, user chooses meal, prints out cooking time, classification, cooking tip, random tip, and profit
def order(options):
    # Displays message and menu for the user to input a menu item
    print("Please enter your order. The options are given below")
    display_menu(options)

    # Validation for the input made by the user - if false, user input will keep being requested
    # Once true, input is converted to an integer
    valid_input = False
    user_input = None
    while not valid_input:
        print("please enter a number to make your choice.")
        user_input = input()
        if validate_user_choice(options, user_input):
            valid_input = True
    user_input = int(user_input)
    
    # Generates a random value for actual cooking time, for the menu item chosen by user
    # Average cook time and stdev of cook time are inputted to gaussian function; random value is outputted
    actual_cook_time = gauss(options[user_input - 1]["cook_time"], options[user_input - 1]["cook_time_stdev"])
    
    # Displays the menu item chose to the user
    print("now cooking", options[user_input - 1]["name"])

    # Classifies cooking time based on average cook time, stdev of cook time, and the random value generated for actual cook time
    # Displays the classification and actual cook time rounded to 2 decimal places, and compare actual vs average cook time.
    classification = classify_cook_time(options[user_input - 1]["cook_time"], options[user_input - 1]["cook_time_stdev"], actual_cook_time)
    print(options[user_input - 1]["name"], "was", classification, "(" + str(round(actual_cook_time,2)), "vs", str(options[user_input - 1]["cook_time"]) + ")" )

    # Calculates cooking tip based on classification and calculates random tip based on random value
    # Default values: base value = 10, tip chance = 10% (0.1), base tip value = 5
    # Then, displays the cooking tip, the random tip, and the random value rounded to 2 decimal places
    cooking_tip = get_cooking_tip(classification, 10)
    random_val = random()
    random_tip = random_tip_compute(0.1, 5, random_val)
    print("cooking tip was", cooking_tip, "random tip was", random_tip, "the random value being", "(" + str(round(random_val,2)) + ")")

    # Calculates selling price based on initial selling price and any cooking/random tip
    # Displays final selling price rounded to 2 decimal places
    selling_price = options[user_input - 1]["sell_for"] * (1 + (cooking_tip + random_tip) / 100)
    print(f"final selling price was ${selling_price:.2f}")

    # Calculates rounded profit by subtracting cost to make from selling price, and rounding off to 2
    # Rounds profit to 2 decimal places, then displays and returns this value
    profit = round((selling_price - options[user_input - 1]["cost_to_make"]), 2)
    print(f"for a profit of ${profit:.2f}")
    return profit

# Executing main function
if __name__ == "__main__":
    order(get_meals_list_from_user())







