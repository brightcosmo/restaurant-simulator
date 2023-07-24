from restaurant_simulator import *
import unittest
from unittest import mock

def run_print_faker(function,*args):
        with mock.patch('sys.stdout') as fake_stdout:
                function(*args)
        string_of_print = convert_calls_to_string(fake_stdout)
        return string_of_print
def run_input_faker(inputs,function):
        original_input = mock.builtins.input
        S = iter(inputs)
        mock.builtins.input = lambda : next(S)
        #setup inputs
        result = function()
        mock.builtins.input = original_input
        return result

def convert_calls_to_string(mock_print):
        the_calls = mock_print.write.call_args_list
        string_calls = []
        for call in the_calls:
                string_calls.append(call[0])
                string_calls[-1] = "".join(string_calls[-1])
        string_calls = "".join(string_calls)
        return string_calls

class TipTests(unittest.TestCase):
    def testTipsStd(self):
        tip = 15
        chance = 0.15
        rnd = 0.13
        observed = random_tip_compute(chance, tip, rnd)
        assert observed == tip, f'Expected random_tip_compute({chance,tip,rnd}) = {tip}; got {observed}'

    def testTipLow(self):
        tip = 1
        chance = 0.35
        rnd = 0.39
        observed = random_tip_compute(chance, tip, rnd)
        assert observed == 0, f'Expected random_tip_compute({chance,tip,rnd}) = 0; got {observed}'

    def testTipHigh(self):
        tip = 99
        chance = 0.02
        rnd = 0.99
        observed = random_tip_compute(chance, tip, rnd)
        assert observed == -tip, f'Expected random_tip_compute({chance,tip,rnd}) = {-tip}; got {observed}'

def dict_equal(d1,d2):
    if len(d1) == len(d2):
        for key in d1:
            if key in d2:
                if (type(d1[key]) == type(dict())) and (type(d2[key]) == type(dict())):
                    result = dict_equal(d1[key],d2[key])
                    if not result:
                        return False
                elif not (d1[key] == d2[key]):
                    return False
            else:
                return False
        return True
    return False
def list_of_dict_equal(l1,l2):
    if len(l1) == len(l2):
        for index in range(len(l1)):
            if not dict_equal(l1[index],l2[index]):
                return False
        return True
    return False

class GetMealTest(unittest.TestCase):
    def testDefault(self):
        inputs = ["."]
        output_list_form =[
            {'name': 'Budda Bowl (vg)', 'sell_for': 25, 'cost_to_make': 20, 'cook_time': 10, 'cook_time_stdev': 3},
            {'name': 'Eye Fillet Steak', 'sell_for': 55, 'cost_to_make': 25, 'cook_time': 7, 'cook_time_stdev': 1},
            {'name': 'Spaghetti Bolognese', 'sell_for': 30, 'cost_to_make': 22, 'cook_time': 40, 'cook_time_stdev': 5},
            {'name': 'Pad Thai (seafood)', 'sell_for': 22, 'cost_to_make': 17, 'cook_time': 30, 'cook_time_stdev': 1}
        ]
        output_dict_form = list_to_num_dict(output_list_form)
        observed = run_input_faker(inputs,get_meals_list_from_user)
        if type(observed) == type([]):
            self.assertTrue(list_of_dict_equal(observed,output_list_form),f'expected {output_list_form} \n but got {observed}')
        elif type(observed) == type(dict()):
            self.assertTrue(dict_equal(observed,output_dict_form),f'expected {output_dict_form} \n but got {observed}')
        else:
            raise AssertionError(f'expected {output_dict_form} (or list equivalent) but got neither a list nor a dictionary')

    def testOneLine(self):
        inputs = ["Peppermint Mango Salsa,15.21,2,5,5","."]
        output_list_form =[
            {'name': 'Peppermint Mango Salsa', 'sell_for': 15.21, 'cost_to_make': 2.0, 'cook_time': 5.0, 'cook_time_stdev': 5.0}
        ]
        output_dict_form = list_to_num_dict(output_list_form)
        observed = run_input_faker(inputs,get_meals_list_from_user)
        if type(observed) == type([]):
            self.assertTrue(list_of_dict_equal(observed,output_list_form),f'expected {output_list_form} \n but got {observed}')
        elif type(observed) == type(dict()):
            self.assertTrue(dict_equal(observed,output_dict_form),f'expected {output_dict_form} \n but got {observed}')
        else:
            raise AssertionError(f'expected {output_dict_form} (or list equivalent) but got neither a list nor a dictionary')

    def testMultiLine(self):
        inputs = ["raw chicken emergency room experience,28.16,15.91,0,0.005",
                  "Peppermint Mango Salsa,15.21,2,5,5",
                  "Popcorn Horseradish Sashimi,115.21,52,19,8",
                  "."
        ]
        output_list_form =[
            {'name': 'raw chicken emergency room experience', 'sell_for': 28.16, 'cost_to_make': 15.91, 'cook_time': 0.0, 'cook_time_stdev': 0.005},
            {'name': 'Peppermint Mango Salsa', 'sell_for': 15.21, 'cost_to_make': 2.0, 'cook_time': 5.0, 'cook_time_stdev': 5.0},
            {'name': 'Popcorn Horseradish Sashimi', 'sell_for': 115.21, 'cost_to_make': 52.0, 'cook_time': 19.0, 'cook_time_stdev': 8.0}
        ]
        output_dict_form = list_to_num_dict(output_list_form)
        observed = run_input_faker(inputs,get_meals_list_from_user)
        if type(observed) == type([]):
            self.assertTrue(list_of_dict_equal(observed,output_list_form),f'expected {output_list_form} \n but got {observed}')
        elif type(observed) == type(dict()):
            self.assertTrue(dict_equal(observed,output_dict_form),f'expected {output_dict_form} \n but got {observed}')
        else:
            raise AssertionError(f'expected {output_dict_form} (or list equivalent) but got neither a list nor a dictionary')

def list_to_num_dict(list_in):
    key = 1
    dict_out = dict()
    for item in list_in:
            dict_out[key] = item
            key+=1
    return dict_out

class GetMenuTest(unittest.TestCase):
    def testDefault(self):
        default_options_list_style = [
            {'name': 'Budda Bowl (vg)', 'sell_for': 25, 'cost_to_make': 20, 'cook_time': 10, 'cook_time_stdev': 3},
            {'name': 'Eye Fillet Steak', 'sell_for': 55, 'cost_to_make': 25, 'cook_time': 7, 'cook_time_stdev': 1},
            {'name': 'Spaghetti Bolognese', 'sell_for': 30, 'cost_to_make': 22, 'cook_time': 40, 'cook_time_stdev': 5},
            {'name': 'Pad Thai (seafood)', 'sell_for': 22, 'cost_to_make': 17, 'cook_time': 30, 'cook_time_stdev': 1}
        ]
        default_options_dict_style = list_to_num_dict(default_options_list_style)
        expected_output = '1. Name:Budda Bowl (vg) Sells:$25 Costs:$20 Takes:10 mins\n2. Name:Eye Fillet Steak Sells:$55 Costs:$25 Takes:7 mins\n3. Name:Spaghetti Bolognese Sells:$30 Costs:$22 Takes:40 mins\n4. Name:Pad Thai (seafood) Sells:$22 Costs:$17 Takes:30 mins\n'
        try:
            observed = run_print_faker(display_menu,default_options_dict_style)
            case1 = expected_output == observed
        except:
            case1 = False
        try:
            observed2 = run_print_faker(display_menu,default_options_list_style)
            case2 = expected_output == observed2
        except:
            case2 = False

        self.assertTrue(case1 or case2)

    def testOneLine(self):
        options_list = [
            {'name': 'Peppermint Mango Salsa', 'sell_for': 15.21, 'cost_to_make': 2.0, 'cook_time': 5.0, 'cook_time_stdev': 5.0}
        ]
        options_dict = list_to_num_dict(options_list)
        expected_output = '1. Name:Peppermint Mango Salsa Sells:$15.21 Costs:$2.0 Takes:5.0 mins\n'
        failed = ""
        got = {"12":"an error"}
        try:
            observed = run_print_faker(display_menu,options_dict)
            case1 = expected_output == observed
            got[""] = observed
            got["2"] = observed
        except:
            case1 = False
            failed += "1"
        try:
            observed2 = run_print_faker(display_menu,options_list)
            case2 = expected_output == observed2
            got["1"] = observed2
        except:
            case2 = False
            failed+= "2"
        self.assertTrue(case1 or case2, f'Expected:{expected_output} but got {got[failed]}')


    def testMultiLine(self):
        options_list = [
            {'name': 'raw chicken emergency room experience', 'sell_for': 28.16, 'cost_to_make': 15.91, 'cook_time': 0.0, 'cook_time_stdev': 0.005},
            {'name': 'Peppermint Mango Salsa', 'sell_for': 15.21, 'cost_to_make': 2.0, 'cook_time': 5.0, 'cook_time_stdev': 5.0},
            {'name': 'Popcorn Horseradish Sashimi', 'sell_for': 115.21, 'cost_to_make': 52.0, 'cook_time': 19.0, 'cook_time_stdev': 8.0}
        ]
        options_dict = list_to_num_dict(options_list)
        expected_output = '1. Name:raw chicken emergency room experience Sells:$28.16 Costs:$15.91 Takes:0.0 mins\n2. Name:Peppermint Mango Salsa Sells:$15.21 Costs:$2.0 Takes:5.0 mins\n3. Name:Popcorn Horseradish Sashimi Sells:$115.21 Costs:$52.0 Takes:19.0 mins\n'
        failed = ""
        got = {"12":"an error"}
        try:
            observed = run_print_faker(display_menu,options_dict)
            case1 = expected_output == observed
            got[""] = observed
            got["2"] = observed
        except:
            case1 = False
            failed += "1"
        try:
            observed2 = run_print_faker(display_menu,options_list)
            case2 = expected_output == observed2
            got["1"] = observed2
        except:
            case2 = False
            failed+= "2"
        self.assertTrue(case1 or case2, f'Expected:{expected_output} but got {got[failed]}')

cooking_time_cases = {
    "mean_cooking_time": 90,
    "stdev_cooking_time": 5,
    # < 80: very undercooked
    # >= 80 and <= 85: slightly undercooked
    # > 85 and < 95: well cooked
    # >= 95 and <= 100: slightly overcooked
    # > 100: very overcooked
    "inputs":[79,80,85,86,90,94,95,100,101],
    "expected":["very undercooked","slightly undercooked","slightly undercooked","well cooked","well cooked","well cooked","slightly overcooked","slightly overcooked","very overcooked"]
}

class CookTimeTest(unittest.TestCase):
    def testNormal0(self):
        test_num = 0
        observed = classify_cook_time(cooking_time_cases["mean_cooking_time"],cooking_time_cases["stdev_cooking_time"],cooking_time_cases["inputs"][test_num])
        assert observed == cooking_time_cases["expected"][test_num], f'Expected classify_cook_time({cooking_time_cases["mean_cooking_time"],cooking_time_cases["stdev_cooking_time"],cooking_time_cases["inputs"][test_num]})=={cooking_time_cases["expected"][test_num]}; got {observed}'

    def testNormal1(self):
        test_num = 1
        observed = classify_cook_time(cooking_time_cases["mean_cooking_time"],cooking_time_cases["stdev_cooking_time"],cooking_time_cases["inputs"][test_num])
        assert observed == cooking_time_cases["expected"][test_num], f'Expected classify_cook_time({cooking_time_cases["mean_cooking_time"],cooking_time_cases["stdev_cooking_time"],cooking_time_cases["inputs"][test_num]})=={cooking_time_cases["expected"][test_num]}; got {observed}'

    def testNormal2(self):
        test_num = 2
        observed = classify_cook_time(cooking_time_cases["mean_cooking_time"],cooking_time_cases["stdev_cooking_time"],cooking_time_cases["inputs"][test_num])
        assert observed == cooking_time_cases["expected"][test_num], f'Expected classify_cook_time({cooking_time_cases["mean_cooking_time"],cooking_time_cases["stdev_cooking_time"],cooking_time_cases["inputs"][test_num]})=={cooking_time_cases["expected"][test_num]}; got {observed}'

    def testNormal3(self):
        test_num = 3
        observed = classify_cook_time(cooking_time_cases["mean_cooking_time"],cooking_time_cases["stdev_cooking_time"],cooking_time_cases["inputs"][test_num])
        assert observed == cooking_time_cases["expected"][test_num], f'Expected classify_cook_time({cooking_time_cases["mean_cooking_time"],cooking_time_cases["stdev_cooking_time"],cooking_time_cases["inputs"][test_num]})=={cooking_time_cases["expected"][test_num]}; got {observed}'

    def testNormal4(self):
        test_num = 4
        observed = classify_cook_time(cooking_time_cases["mean_cooking_time"],cooking_time_cases["stdev_cooking_time"],cooking_time_cases["inputs"][test_num])
        assert observed == cooking_time_cases["expected"][test_num], f'Expected classify_cook_time({cooking_time_cases["mean_cooking_time"],cooking_time_cases["stdev_cooking_time"],cooking_time_cases["inputs"][test_num]})=={cooking_time_cases["expected"][test_num]}; got {observed}'

    def testNormal5(self):
        test_num = 5
        observed = classify_cook_time(cooking_time_cases["mean_cooking_time"],cooking_time_cases["stdev_cooking_time"],cooking_time_cases["inputs"][test_num])
        assert observed == cooking_time_cases["expected"][test_num], f'Expected classify_cook_time({cooking_time_cases["mean_cooking_time"],cooking_time_cases["stdev_cooking_time"],cooking_time_cases["inputs"][test_num]})=={cooking_time_cases["expected"][test_num]}; got {observed}'

    def testNormal6(self):
        test_num = 6
        observed = classify_cook_time(cooking_time_cases["mean_cooking_time"],cooking_time_cases["stdev_cooking_time"],cooking_time_cases["inputs"][test_num])
        assert observed == cooking_time_cases["expected"][test_num], f'Expected classify_cook_time({cooking_time_cases["mean_cooking_time"],cooking_time_cases["stdev_cooking_time"],cooking_time_cases["inputs"][test_num]})=={cooking_time_cases["expected"][test_num]}; got {observed}'

cooking_tip_cases = {
    "base_tip": 19,
    "classifications":["slightly undercooked","very undercooked","slightly overcooked","very overcooked","well cooked","well cooked","well cooked"],
    "expected":[0,-100,0,-100,19,19,19]
}

class CookTipTest(unittest.TestCase):
    def testTip0(self):
        test_num = 0
        observed = get_cooking_tip(cooking_tip_cases["classifications"][test_num], cooking_tip_cases["base_tip"])
        assert observed == cooking_tip_cases["expected"][test_num], f'Expected cook_meal({cooking_tip_cases["classifications"][test_num],cooking_tip_cases["base_tip"]})=={cooking_tip_cases["expected"][test_num]}; got {observed}'

    def testTip1(self):
        test_num = 1
        observed = get_cooking_tip(cooking_tip_cases["classifications"][test_num], cooking_tip_cases["base_tip"])
        assert observed == cooking_tip_cases["expected"][test_num], f'Expected cook_meal({cooking_tip_cases["classifications"][test_num],cooking_tip_cases["base_tip"]})=={cooking_tip_cases["expected"][test_num]}; got {observed}'
    def testTip2(self):
        test_num = 2
        observed = get_cooking_tip(cooking_tip_cases["classifications"][test_num], cooking_tip_cases["base_tip"])
        assert observed == cooking_tip_cases["expected"][test_num], f'Expected cook_meal({cooking_tip_cases["classifications"][test_num],cooking_tip_cases["base_tip"]})=={cooking_tip_cases["expected"][test_num]}; got {observed}'
    def testTip3(self):
        test_num = 3
        observed = get_cooking_tip(cooking_tip_cases["classifications"][test_num], cooking_tip_cases["base_tip"])
        assert observed == cooking_tip_cases["expected"][test_num], f'Expected cook_meal({cooking_tip_cases["classifications"][test_num],cooking_tip_cases["base_tip"]})=={cooking_tip_cases["expected"][test_num]}; got {observed}'
    def testTip4(self):
        test_num = 4
        observed = get_cooking_tip(cooking_tip_cases["classifications"][test_num], cooking_tip_cases["base_tip"])
        assert observed == cooking_tip_cases["expected"][test_num], f'Expected cook_meal({cooking_tip_cases["classifications"][test_num],cooking_tip_cases["base_tip"]})=={cooking_tip_cases["expected"][test_num]}; got {observed}'
    def testTip5(self):
        test_num = 5
        observed = get_cooking_tip(cooking_tip_cases["classifications"][test_num], cooking_tip_cases["base_tip"])
        assert observed == cooking_tip_cases["expected"][test_num], f'Expected cook_meal({cooking_tip_cases["classifications"][test_num],cooking_tip_cases["base_tip"]})=={cooking_tip_cases["expected"][test_num]}; got {observed}'
    def testTip6(self):
        test_num = 6
        observed = get_cooking_tip(cooking_tip_cases["classifications"][test_num], cooking_tip_cases["base_tip"])
        assert observed == cooking_tip_cases["expected"][test_num], f'Expected cook_meal({cooking_tip_cases["classifications"][test_num],cooking_tip_cases["base_tip"]})=={cooking_tip_cases["expected"][test_num]}; got {observed}'

validations_cases = {
    "valids": ["1","2","3","4"],
    "invalids":["","-4","77","fdsfdss"],
    "options": ["sample","another sample","something else","last thing"]
}
class choiceValidateTest(unittest.TestCase):
    def testValid0(self):
        case_num = 0
        observed = validate_user_choice(validations_cases["options"],validations_cases["valids"][case_num])
        assert observed, f'Expected validateUserChoice({validations_cases["options"],validations_cases["valids"][case_num]})==True; got {observed}'
    def testValid1(self):
        case_num = 1
        observed = validate_user_choice(validations_cases["options"],validations_cases["valids"][case_num])
        assert observed, f'Expected validateUserChoice({validations_cases["options"],validations_cases["valids"][case_num]})==True; got {observed}'
    def testValid2(self):
        case_num = 2
        observed = validate_user_choice(validations_cases["options"],validations_cases["valids"][case_num])
        assert observed, f'Expected validateUserChoice({validations_cases["options"],validations_cases["valids"][case_num]})==True; got {observed}'
    def testValid3(self):
        case_num = 3
        observed = validate_user_choice(validations_cases["options"],validations_cases["valids"][case_num])
        assert observed, f'Expected validateUserChoice({validations_cases["options"],validations_cases["valids"][case_num]})==True; got {observed}'
    def testInvalid0(self):
        case_num = 0
        observed = validate_user_choice(validations_cases["options"],validations_cases["invalids"][case_num])
        assert not observed, f'Expected validateUserChoice({validations_cases["options"],validations_cases["invalids"][case_num]})==False; got {observed}'
    def testInvalid1(self):
        case_num = 1
        observed = validate_user_choice(validations_cases["options"],validations_cases["invalids"][case_num])
        assert not observed, f'Expected validateUserChoice({validations_cases["options"],validations_cases["invalids"][case_num]})==False; got {observed}'
    def testInvalid2(self):
        case_num = 2
        observed = validate_user_choice(validations_cases["options"],validations_cases["invalids"][case_num])
        assert not observed, f'Expected validateUserChoice({validations_cases["options"],validations_cases["invalids"][case_num]})==False; got {observed}'
    def testInvalid3(self):
        case_num = 3
        observed = validate_user_choice(validations_cases["options"],validations_cases["invalids"][case_num])
        assert not observed, f'Expected validateUserChoice({validations_cases["options"],validations_cases["invalids"][case_num]})==False; got {observed}'


if __name__=="__main__":
        unittest.main()
        
