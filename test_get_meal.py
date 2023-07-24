import unittest
from typing import TextIO
from unittest import mock
from unittest.mock import patch
filename = "get_meal.py"
test_list = [
{"inputs":["."],"output_lines":[[]]},
{"inputs":["Peppermint Mango Salsa,15.21,2,5,5","."],"output_lines":[[{'name': 'Peppermint Mango Salsa', 'sell_for': 15.21, 'cost_to_make': 2.0, 'cook_time': 5.0, 'cook_time_stdev': 5.0}]]},
{"inputs":["raw chicken emergency room experience,28.16,15.91,0,0.005","Peppermint Mango Salsa,15.21,2,2,0.2","."],"output_lines":[[{'name': 'raw chicken emergency room experience', 'sell_for': 28.16, 'cost_to_make': 15.91, 'cook_time': 0.0, 'cook_time_stdev': 0.005}, {'name': 'Peppermint Mango Salsa', 'sell_for': 15.21, 'cost_to_make': 2.0, 'cook_time': 2.0, 'cook_time_stdev': 0.2}]
]}
]
original_input = mock.builtins.input

def mock_up_input(data):
        S = iter(data)
        mock.builtins.input = lambda : next(S)

def retreive_input():
        mock.builtins.input = original_input

def run_input_tester(inputs):
        mock_up_input(inputs)
        #setup inputs
        with mock.patch('sys.stdout') as fake_stdout:
                file = open(filename)
                exec(file.read())
                file.close()
        retreive_input()
        return fake_stdout

def runTestX(index):
        this_test = test_list[index]
        observed = run_input_tester(this_test["inputs"])
        expected = []
        for outs in this_test["output_lines"]:
                expected.append(mock.call.write(str(outs)))
        return [observed,expected]

class TestIOFile(unittest.TestCase):
        def testEmpty(self):
                observed,expected = runTestX(0)
                observed.assert_has_calls(expected)
        def testOneList(self):
                observed,expected = runTestX(1)
                observed.assert_has_calls(expected)
        def testTwoList(self):
                observed,expected = runTestX(2)
                observed.assert_has_calls(expected)

if __name__=="__main__":
        unittest.main()

