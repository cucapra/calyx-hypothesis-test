import subprocess
import json
from hypothesis import given, note, settings, strategies as st
import logging
import os


# step 1: build a hypothesis framework for addition
# step 2: take hypothesis generated width, input_1, input_2 and write them into data.json
# step 3: execute shell command
# step 4: compute addition result using python (consider width) and compare with the shell result

# TEST: fud e --to dat examples/hypothesis-test/language-tutorial-iterate.futil -s verilog.data
# examples/tutorial/data.json --through icarus-verilog

def construct_not_json(x):
    false = False
    my_input = {
        "inp": {
            "data": [x, 0],
            "format": {
                "numeric_type": "bitnum",
                "is_signed": false,
                "width": 32
            }
        }
    }
    return my_input


@given(x=st.integers(min_value=0, max_value=2 ** 32 - 1))
@settings(deadline=None)
def test_not(x):
    # write x to data
    # note(f"Testing with inputs: {x!r} and {y!r}, width: 32")
    input_data = construct_not_json(x)
    with open('data.json', 'w') as json_file:
        json.dump(input_data, json_file)
    subprocess.Popen(["cd", "/Users/crystalhu/Calyx"], env=dict(os.environ))
    os.system("fud e add.futil -s verilog.data data.json --to dat -q --through icarus-verilog > result.json")
    # read result from data
    try:
        with open('result.json') as f_2:
            result_data = json.load(f_2)
            res = result_data['memories']['inp'][2]
            assert (res == (x + y) % 32)
    except Exception as e:
        logging.error(e)


# assert result = (x + y) mod width


def construct_and_json(x, y):
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
def test_and(x, y):
    # write x and y to data
    # note(f"Testing with inputs: {x!r} and {y!r}, width: 32")
    input_data = construct_and_json(x, y)
    with open('data.json', 'w') as json_file:
        json.dump(input_data, json_file)
    os.system("fud e and.futil -s verilog.data data.json --to dat -q --through icarus-verilog > result.json")
    # read result from data
    try:
        with open('result.json') as f_2:
            result_data = json.load(f_2)
            res = result_data['memories']['inp'][2]
            assert (res == x & y)
    except Exception as e:
        note(type(e))


# assert result = (x + y) mod width
# execute through icarus verilog
# os.system('fud e add.futil -s verilog.data data.json --to dat -q --through icarus-verilog')

if __name__ == "__main__":
    test_not()
    test_and()
