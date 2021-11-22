import json
from hypothesis import given, settings, strategies as st
import logging
import os


def construct_json(x, y):
    true = True
    my_input = {
        "inp": {
            "data": [x, y, 0],
            "format": {
                "numeric_type": "bitnum",
                "is_signed": true,
                "width": 32
            }
        }
    }
    return my_input


@given(x=st.integers(min_value=-2 ** 31 + 1, max_value=2 ** 31 - 1),
       y=st.integers(min_value=-2 ** 31 + 1, max_value=2 ** 31 - 1))
@settings(deadline=None)
def test_sadd(x, y):
    input_data = construct_json(x, y)
    with open('data.json', 'w') as json_file:
        json.dump(input_data, json_file)
    os.system("fud e std_sadd.futil -s verilog.data data.json --to dat -q --through icarus-verilog > result.json")
    try:
        with open('result.json') as f_2:
            result_data = json.load(f_2)
            s = result_data['memories']['inp'][2]
            if s > 0:
                assert s == (x + y) % (2 ** 31), "positive sum wrong."
            else:
                assert s == (x + y) % (-2 ** 31), "negative sum wrong."
                logging.info("Success.")
    except ArithmeticError as ae:
        logging.error(ae)
    except Exception as e:
        logging.error(f'error is: {e}')
        logging.error(f'fail with x = {x}, y = {y}, sum = {s}')


if __name__ == "__main__":
    test_sadd()
