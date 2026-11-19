import pytest
from youtube_dl.aes import shift_rows

def test_shift_rows_basic():
    # 16-byte input where each byte is its index
    data = list(range(16))
    # Expected output computed manually:
    # Column 0: rows 0-3 -> indices 0,4,8,12
    # Column 1: rows 0-3 -> indices 1,5,9,13
    # Column 2: rows 0-3 -> indices 2,6,10,14
    # Column 3: rows 0-3 -> indices 3,7,11,15
    expected = [0,4,8,12, 1,5,9,13, 2,6,10,14, 3,7,11,15]
    assert shift_rows(data) == expected

def test_shift_rows_with_pattern():
    # Input with repeating pattern to verify shifting
    data = [0x00, 0x01, 0x02, 0x03,
            0x10, 0x11, 0x12, 0x13,
            0x20, 0x21, 0x22, 0x23,
            0x30, 0x31, 0x32, 0x33]
    # Expected output: each column rotated by its row index
    expected = [0x00, 0x10, 0x20, 0x30,
                0x01, 0x11, 0x21, 0x31,
                0x02, 0x12, 0x22, 0x32,
                0x03, 0x13, 0x23, 0x33]
    assert shift_rows(data) == expected

def test_shift_rows_invalid_length():
    # Provide fewer than 16 bytes; should raise IndexError
    data = [0] * 12  # too short
    with pytest.raises(IndexError):
        shift_rows(data)
