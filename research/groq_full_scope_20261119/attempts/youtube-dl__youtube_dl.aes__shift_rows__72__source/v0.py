import pytest
from youtube_dl.aes import shift_rows

def test_shift_rows_basic():
    # Input is a 4x4 matrix flattened row-major:
    # 00 01 02 03
    # 04 05 06 07
    # 08 09 10 11
    # 12 13 14 15
    data = list(range(16))
    # Expected output after shift_rows:
    # 00 04 08 12
    # 01 05 09 13
    # 02 06 10 14
    # 03 07 11 15
    expected = [
        0, 4, 8, 12,
        1, 5, 9, 13,
        2, 6,10, 14,
        3, 7,11, 15
    ]
    assert shift_rows(data) == expected

def test_shift_rows_identity_on_identity():
    # Identity matrix where each element equals its index
    data = [i for i in range(16)]
    # For this specific pattern, shift_rows should produce the same list
    # because each row is a shift of the previous by one.
    assert shift_rows(data) == data

def test_shift_rows_invalid_length_raises():
    # Providing fewer than 16 bytes should raise an IndexError
    data = [0] * 10
    with pytest.raises(IndexError):
        shift_rows(data)
