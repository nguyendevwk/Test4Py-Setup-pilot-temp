import pytest
from youtube_dl.aes import shift_rows

def test_shift_rows_basic():
    # 16-byte input where each byte is its index
    data = list(range(16))
    # Expected output computed manually:
    # Column 0: rows 0-3 -> indices 0,4,8,12
    # Column 1: rows 0-3 -> indices 5,1,9,13
    # Column 2: rows 0-3 -> indices 10,6,2,14
    # Column 3: rows 0-3 -> indices 15,11,7,3
    expected = [0, 4, 8, 12, 5, 1, 9, 13, 10, 6, 2, 14, 15, 11, 7, 3]
    assert shift_rows(data) == expected

def test_shift_rows_all_zeros():
    data = [0] * 16
    # Shifting zeros should still produce all zeros
    assert shift_rows(data) == [0] * 16

def test_shift_rows_invalid_length():
    # Provide fewer than 16 bytes; should raise IndexError due to out-of-range access
    data = list(range(10))
    with pytest.raises(IndexError):
        shift_rows(data)
