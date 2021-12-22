import json
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
        "Sum0": {
            "data": [0, 0, 0, 0, 0, 0, 0, 0],
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
def test_vector_add(x_lst, y_lst):
    input_data = construct_json(x_lst, y_lst)
    with open('data.json', 'w') as json_file:
        json.dump(input_data, json_file)
    try:
        os.system("fud e vectorized_add.futil -s verilog.data data.json --to dat -q --through icarus-verilog > "
                  "result.json")
        with open('result.json') as f_2:
            result_data = json.load(f_2)
            result = result_data['memories']['Sum0']
            py_sum = [x+y for x, y in zip(x_lst, y_lst)]
            for i in range(len(result)):
                if py_sum[i] < 0:
                    assert result[i] == py_sum[i] % (-2 ** 31), "negative sum wrong."
                else:
                    assert result[i] == py_sum[i] % (2 ** 31), "positive sum wrong."
    except ArithmeticError as ae:
        logging.error(ae)
    except Exception as e:
        logging.error(f'fail with error {e}')
        logging.error(f'fail with x = {x_lst}, y = {y_lst}, sum = {result}.')


if __name__ == "__main__":
    test_vector_add()
