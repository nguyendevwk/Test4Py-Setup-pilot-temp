import pytest
from youtube_dl.aes import shift_rows_inv

def test_shift_rows_inv_known_pattern():
    # Input: 4x4 matrix in column-major order
    # Matrix:
    # 00 04 08 12
    # 01 05 09 13
    # 02 06 10 14
    # 03 07 11 15
    data = [
        0x00, 0x01, 0x02, 0x03,
        0x04, 0x05, 0x06, 0x07,
        0x08, 0x09, 0x0A, 0x0B,
        0x0C, 0x0D, 0x0E, 0x0F
    ]
    # Expected inverse shift rows result:
    # 00 01 02 03
    # 04 05 06 07
    # 08 09 0A 0B
    # 0C 0D 0E 0F
    # After inverse shift rows, the matrix should be:
    # 00 04 08 0C
    # 01 05 09 0D
    # 02 06 0A 0E
    # 03 07 0B 0F
    expected = [
        0x00, 0x04, 0x08, 0x0C,
        0x01, 0x05, 0x09, 0x0D,
        0x02, 0x06, 0x0A, 0x0E,
        0x03, 0x07, 0x0B, 0x0F
    ]
    result = shift_rows_inv(data)
    assert result == expected, f"Expected {expected}, got {result}"

def test_shift_rows_inv_all_zeros():
    data = [0] * 16
    result = shift_rows_inv(data)
    assert result == data, "All-zero input should return all-zero output"

def test_shift_rows_inv_invalid_length():
    # Provide a list shorter than required; should raise IndexError
    data = [0] * 10
    with pytest.raises(IndexError):
        shift_rows_inv(data)
