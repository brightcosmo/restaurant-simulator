import unittest
from typing import TextIO
from unittest import mock
from unittest.mock import patch
filename = "get_menu.py"
test_list = [
{"inputs":["."],"output_lines":'1. Name:Budda Bowl (vg) Sells:$25.0 Costs:$20.0 Takes:10.0 mins\n2. Name:Eye Fillet Steak Sells:$55.0 Costs:$25.0 Takes:7.0 mins\n3. Name:Spaghetti Bolognese Sells:$30.0 Costs:$22.0 Takes:40.0 mins\n4. Name:Pad Thai (seafood) Sells:$22.0 Costs:$17.0 Takes:30.0 mins\n'},
{"inputs":["Peppermint Mango Salsa,15.21,2,5,5","."],"output_lines":'1. Name:Peppermint Mango Salsa Sells:$15.21 Costs:$2.0 Takes:5.0 mins\n'},
{"inputs":["raw chicken emergency room experience,28.16,15.91,0,0.005","Peppermint Mango Salsa,15.21,2,5,5","."],"output_lines":'1. Name:raw chicken emergency room experience Sells:$28.16 Costs:$15.91 Takes:0.0 mins\n2. Name:Peppermint Mango Salsa Sells:$15.21 Costs:$2.0 Takes:5.0 mins\n'}
]

def run_input_tester(inputs):
        original_input = mock.builtins.input
        S = iter(inputs)
        mock.builtins.input = lambda : next(S)
        #setup inputs
        with mock.patch('sys.stdout') as fake_stdout:
                file = open(filename)
                exec(file.read())
                file.close()
        mock.builtins.input = original_input
        return fake_stdout

def runTestX(index):
        this_test = test_list[index]
        observed = run_input_tester(this_test["inputs"])
        observed = convert_calls_to_string(observed)
        return [observed,this_test["output_lines"]]

def convert_calls_to_string(mock_print):
        the_calls = mock_print.write.call_args_list
        string_calls = []
        for call in the_calls:
                string_calls.append(call[0])
                string_calls[-1] = "".join(string_calls[-1])
        string_calls = "".join(string_calls)
        return string_calls

class TestIOFile(unittest.TestCase):
        def testEmpty(self):
                observed,expected = runTestX(0)
                self.assertEqual(observed,expected)

        def testOneList(self):
                observed,expected = runTestX(1)
                self.assertEqual(observed,expected)
        def testTwoList(self):
                observed,expected = runTestX(2)
                self.assertEqual(observed,expected)

if __name__=="__main__":
        unittest.main()

