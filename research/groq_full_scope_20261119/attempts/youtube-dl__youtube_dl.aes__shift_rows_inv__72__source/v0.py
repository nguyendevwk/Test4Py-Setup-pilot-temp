import pytest
from youtube_dl.aes import shift_rows_inv

def test_shift_rows_inv_basic_mapping():
    # 16-byte input where each byte is its index value
    data = list(range(16))
    # Expected output computed manually:
    # For each column (0-3) and row (0-3):
    # index = ((column - row) & 0b11) * 4 + row
    expected = [
        data[((0 - 0) & 0b11) * 4 + 0],  # 0
        data[((0 - 1) & 0b11) * 4 + 1],  # 13
        data[((0 - 2) & 0b11) * 4 + 2],  # 10
        data[((0 - 3) & 0b11) * 4 + 3],  # 7
        data[((1 - 0) & 0b11) * 4 + 0],  # 4
        data[((1 - 1) & 0b11) * 4 + 1],  # 1
        data[((1 - 2) & 0b11) * 4 + 2],  # 14
        data[((1 - 3) & 0b11) * 4 + 3],  # 11
        data[((2 - 0) & 0b11) * 4 + 0],  # 8
        data[((2 - 1) & 0b11) * 4 + 1],  # 5
        data[((2 - 2) & 0b11) * 4 + 2],  # 2
        data[((2 - 3) & 0b11) * 4 + 3],  # 15
        data[((3 - 0) & 0b11) * 4 + 0],  # 12
        data[((3 - 1) & 0b11) * 4 + 1],  # 9
        data[((3 - 2) & 0b11) * 4 + 2],  # 6
        data[((3 - 3) & 0b11) * 4 + 3],  # 3
    ]
    result = shift_rows_inv(data)
    assert result == expected
    assert len(result) == 16

def test_shift_rows_inv_identity_on_zeroes():
    # All zeros should remain zeros after transformation
    data = [0] * 16
    result = shift_rows_inv(data)
    assert result == data
    assert all(b == 0 for b in result)

def test_shift_rows_inv_invalid_length_raises():
    # Providing fewer than 16 bytes should raise an IndexError
    data = list(range(10))  # too short
    with pytest.raises(IndexError):
        shift_rows_inv(data)
