import pytest
from youtube_dl.aes import shift_rows_inv

def test_shift_rows_inv_known_vector():
    """Verify that shift_rows_inv produces the expected permutation for a sequential input."""
    input_data = list(range(16))
    expected_output = [
        0, 13, 10, 7,
        4, 1, 14, 11,
        8, 5, 2, 15,
        12, 9, 6, 3
    ]
    assert shift_rows_inv(input_data) == expected_output

def test_shift_rows_inv_short_input_raises():
    """shift_rows_inv should raise an IndexError when the input list is too short."""
    short_input = list(range(15))  # one element missing
    with pytest.raises(IndexError):
        shift_rows_inv(short_input)

def test_shift_rows_inv_all_zeros():
    """shift_rows_inv should return all zeros when given an all-zero input."""
    zeros_input = [0] * 16
    assert shift_rows_inv(zeros_input) == [0] * 16
