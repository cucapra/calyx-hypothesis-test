import subprocess
import json
from hypothesis import given, settings, strategies as st
import logging
import os


# step 1: build a hypothesis framework for addition
# step 2: take hypothesis generated width, input_1, input_2 and write them into data.json
# step 3: execute shell command
# step 4: compute addition result using python (consider width) and compare with the shell result

# TEST: fud e --to dat examples/hypothesis-test/language-tutorial-iterate.futil -s verilog.data
# examples/tutorial/data.json --through icarus-verilog

def construct_json(x, y):
    false = False
    my_input = {
        "inp": {
            "data": [x, y, 0],
            "format": {
                "numeric_type": "bitnum",
                "is_signed": false,
                "width": 32
            }
        }
    }
    return my_input


@given(x=st.integers(min_value=0, max_value=2 ** 32 - 1), y=st.integers(min_value=0, max_value=2 ** 32 - 1))
@settings(deadline=None)
def test_addition(x, y):
    # write x and y to data
    # note(f"Testing with inputs: {x!r} and {y!r}, width: 32")
    input_data = construct_json(x, y)
    my_env = os.environ
    with open('data.json', 'w') as json_file:
        json.dump(input_data, json_file)
    subprocess.Popen(["cd", "/Users/crystalhu/Calyx"], env=dict(os.environ))
    os.system("fud e std_add.futil -s verilog.data data.json --to dat -q --through icarus-verilog > result.json")
    # read result from data
    try:
        with open('result.json') as f_2:
            result_data = json.load(f_2)
            res = result_data['memories']['inp'][2]
            assert (res == (x + y) % (2 ** 32))
    except Exception as e:
        logging.error(f'fail with x = {x}, y = {y}, and result = {res}. Expect {(x + y) % 32}')
# assert result = (x + y) mod width


# execute through icarus verilog
# os.system('fud e std_add.futil -s verilog.data data.json --to dat -q --through icarus-verilog')

if __name__ == "__main__":
    test_addition()
