import unittest
from typing import TextIO
from unittest import mock
from unittest.mock import patch
filename = "classify_cooking_for_tip.py"
test_list = [
{"inputs":["raw chicken emergency room experience,28.16,15.91,0,0.005","Peppermint Mango Salsa,15.21,2,5,5","Chocolate,1,2,3,1","Banana,5,6,7,8","Feta,9,10,11,12",".","3,3"],"output_lines":'Chocolate was well cooked and cooking tip was 10%\n'},
{"inputs":["raw chicken emergency room experience,28.16,15.91,0,0.005","Peppermint Mango Salsa,15.21,2,5,5","Chocolate,1,2,3,1","Banana,5,6,7,8","Feta,9,10,11,12",".","3,1.9"],"output_lines":'Chocolate was slightly undercooked and cooking tip was 0%\n'},
{"inputs":["raw chicken emergency room experience,28.16,15.91,0,0.005","Peppermint Mango Salsa,15.21,2,5,5","Chocolate,1,2,3,1","Banana,5,6,7,8","Feta,9,10,11,12",".","3,0.9"],"output_lines":'Chocolate was very undercooked and cooking tip was -100%\n'},
{"inputs":["raw chicken emergency room experience,28.16,15.91,0,0.005","Peppermint Mango Salsa,15.21,2,5,5","Chocolate,1,2,3,1","Banana,5,6,7,8","Feta,9,10,11,12",".","3,4.1"],"output_lines":'Chocolate was slightly overcooked and cooking tip was 0%\n'},
{"inputs":["raw chicken emergency room experience,28.16,15.91,0,0.005","Peppermint Mango Salsa,15.21,2,5,5","Chocolate,1,2,3,1","Banana,5,6,7,8","Feta,9,10,11,12",".","3,5.1"],"output_lines":'Chocolate was very overcooked and cooking tip was -100%\n'}
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
        def testWell(self):
                observed,expected = runTestX(0)
                self.assertEqual(observed,expected)
        def testSlightUnder(self):
                observed,expected = runTestX(1)
                self.assertEqual(observed,expected)
        def testVeryUnder(self):
                observed,expected = runTestX(2)
                self.assertEqual(observed,expected)
        def testSlightOver(self):
                observed,expected = runTestX(3)
                self.assertEqual(observed,expected)
        def testVeryOver(self):
                observed,expected = runTestX(4)
                self.assertEqual(observed,expected)

if __name__=="__main__":
        unittest.main()

