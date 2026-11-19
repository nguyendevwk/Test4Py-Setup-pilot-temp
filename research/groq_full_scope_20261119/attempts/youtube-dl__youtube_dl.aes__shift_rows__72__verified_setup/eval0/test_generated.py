import pytest
from youtube_dl.aes import shift_rows

def test_shift_rows_known_pattern():
    # Input: 0,1,2,...,15
    data = list(range(16))
    # Expected output computed manually:
    # Column 0: rows 0-3 -> indices 0,4,8,12
    # Column 1: rows 0-3 -> indices 1,5,9,13
    # Column 2: rows 0-3 -> indices 2,6,10,14
    # Column 3: rows 0-3 -> indices 3,7,11,15
    expected = [0, 4, 8, 12,
                1, 5, 9, 13,
                2, 6, 10, 14,
                3, 7, 11, 15]
    assert shift_rows(data) == expected

def test_shift_rows_all_zeros():
    data = [0] * 16
    assert shift_rows(data) == [0] * 16

def test_shift_rows_invalid_length_raises():
    # Provide fewer than 16 elements to trigger an IndexError
    data = list(range(10))
    with pytest.raises(IndexError):
        shift_rows(data)
