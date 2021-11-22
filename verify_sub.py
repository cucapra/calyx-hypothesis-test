import json
from hypothesis import given, settings, strategies as st
import logging
import os

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
    with open('data.json', 'w') as json_file:
        json.dump(input_data, json_file)
    os.system("fud e std_sub.futil -s verilog.data data.json --to dat -q --through icarus-verilog > result.json")
    try:
        with open('result.json') as f_2:
            result_data = json.load(f_2)
            s = result_data['memories']['inp'][2]
            assert s == (x - y) % (2 ** 32), "difference wrong."
            logging.info("Success.")
    except ArithmeticError as ae:
        logging.error(ae)
    except Exception as e:
        logging.error(f'error is: {e}')
        logging.error(f'fail with x = {x}, y = {y}, difference = {s}')


# assert result = (x + y) mod width


# execute through icarus verilog
# os.system('fud e add.futil -s verilog.data data.json --to dat -q --through icarus-verilog')

if __name__ == "__main__":
    test_addition()
