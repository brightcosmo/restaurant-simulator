# Creates a new list for the meal options
options = []

while True:
    # Takes in menu details as input separated by ","
    meal_data = input().split(",")

    # While loop will end and inputs will stop once "." is inputted
    if meal_data == ["."]:
        break

    # Adds inputted menu details to the list, converting numeric data types to float
    options.append({
        "name": meal_data[0],
        "sell_for": float(meal_data[1]),
        "cost_to_make": float(meal_data[2]),
        "cook_time": float(meal_data[3]),
        "cook_time_stdev": float(meal_data[4])
    })

# Prints the meal details
print(options)
#python get_meal.py
#python test_get_meal.py
