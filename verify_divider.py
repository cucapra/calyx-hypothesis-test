import json
from hypothesis import given, settings, strategies as st
import logging
import os


def construct_json(x_lst, y_lst):
    true = True
    my_input = {
        "left": {
            "data": x_lst,
            "format": {
                "numeric_type": "bitnum",
                "is_signed": true,
                "width": 32
            }
        },
        "right": {
            "data": y_lst,
            "format": {
                "numeric_type": "bitnum",
                "is_signed": true,
                "width": 32
            }
        },
        "out_rem": {
            "data": [0, 0, 0, 0],
            "format": {
                "numeric_type": "bitnum",
                "is_signed": true,
                "width": 32
            }
        },
        "out_quot": {
            "data": [0, 0, 0, 0],
            "format": {
                "numeric_type": "bitnum",
                "is_signed": true,
                "width": 32
            }
        }
    }
    return my_input


@given(x0=st.integers(min_value=-2 ** 31 + 1, max_value=-1),
       x1=st.integers(min_value=0, max_value=2 ** 31 - 1),
       x2=st.integers(min_value=-2 ** 31 + 1, max_value=-1),
       x3=st.integers(min_value=0, max_value=2 ** 31 - 1),
       y0=st.integers(min_value=-2 ** 31 + 1, max_value=-1),
       y2=st.integers(min_value=0, max_value=2 ** 31 - 1),
       y1=st.integers(min_value=-2 ** 31 + 1, max_value=-1),
       y3=st.integers(min_value=0, max_value=2 ** 31 - 1))
@settings(deadline=None)
def test_sdivider(x0, x1, x2, x3, y0, y1, y2, y3):
    x_lst = [x0, x1, x2, x3]
    y_lst = [y0, y1, y2, y3]
    input_data = construct_json(x_lst, y_lst)
    with open('data.json', 'w') as json_file:
        json.dump(input_data, json_file)
    try:
        os.system("fud e std_sdiv.futil -s verilog.data data.json --to dat -q --through icarus-verilog > "
                  "result.json")
        # read result from data
        with open('result.json') as f_2:
            result_data = json.load(f_2)
            quot = result_data['memories']['out_quot']
            rem = result_data['memories']['out_rem']
            for i in range(len(quot)):
                if quot[i] * y_lst[i] + rem[i] > 0:
                    assert (quot[i] * y_lst[i] + rem[i]) % (2 ** 31) == x_lst[i], f'positive assert error at index {i} expect A = {quot[i] * y_lst[i] + rem[i]} '
                else:
                    assert (quot[i] * y_lst[i] + rem[i]) % (-2 ** 31) == x_lst[i], f'positive assert error at index {i} expect A = {quot[i] * y_lst[i] + rem[i]} '
                logging.info("Success.")
    except ArithmeticError as ae:
        logging.error(ae)
    except Exception as e:
        logging.error(f'fail with error {e}')
        logging.error(f'fail with x = {x_lst}, y = {y_lst}, quo = {quot}, rem = {rem}.')


if __name__ == "__main__":
    test_sdivider()
