# Imports required modules from 'random'
from random import gauss, random

# Obtains input for actual cooking time and standard deviation
cooking_times = input().split(",")
correct_time = float(cooking_times[0])
time_stdev = float(cooking_times[1])

def get_tip() -> str:
    # Returns random tip to print
    random_num = random()
    if random_num < 0.1:
        return "5%"
    elif random_num >= 0.1 and random_num < 0.9:
        return "0%"
    else:
        return "-5%"

# Prints actual cooking time and tip
print("Actual cooking time was", gauss(correct_time, time_stdev), "and the tip paid was", get_tip())
