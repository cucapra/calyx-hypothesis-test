import json
import numpy
from hypothesis import given, settings, strategies as st
import logging
import os


def construct_json(x_lst, y_lst):
    true = True
    my_input = {
        "A0": {
            "data": x_lst,
            "format": {
                "numeric_type": "bitnum",
                "is_signed": true,
                "width": 32
            }
        },
        "B0": {
            "data": y_lst,
            "format": {
                "numeric_type": "bitnum",
                "is_signed": true,
                "width": 32
            }
        },
        "v0": {
            "data": [0],
            "format": {
                "numeric_type": "bitnum",
                "is_signed": true,
                "width": 32
            }
        }
    }
    return my_input


@given(x_lst=st.lists(st.integers(min_value=-2 ** 31 + 1, max_value=2 ** 31 - 1), min_size=8, max_size=8),
       y_lst=st.lists(st.integers(min_value=-2 ** 31 + 1, max_value=2 ** 31 - 1), min_size=8, max_size=8))
@settings(deadline=None)
def test_dot_product(x_lst, y_lst):
    input_data = construct_json(x_lst, y_lst)
    with open('data.json', 'w') as json_file:
        json.dump(input_data, json_file)
    try:
        os.system("fud e dot_product.futil -s verilog.data data.json --to dat -q --through icarus-verilog > "
                  "result.json")
        # read result from data
        with open('result.json') as f_2:
            result_data = json.load(f_2)
            v = result_data['memories']['v0']
            assert numpy.dot(x_lst, y_lst) == v % (2 ** 31)
    except ArithmeticError as ae:
        logging.error(ae)
    except Exception as e:
        logging.error(f'fail with error {e}')
        logging.error(f'fail with x = {x_lst}, y = {y_lst}, v{v}.')


if __name__ == "__main__":
    test_dot_product()
