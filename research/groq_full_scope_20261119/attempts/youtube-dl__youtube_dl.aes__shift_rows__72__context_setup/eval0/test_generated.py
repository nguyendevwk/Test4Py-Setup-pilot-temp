import pytest
from youtube_dl.aes import shift_rows

def test_shift_rows_basic():
    # Input: 4x4 matrix in column-major order
    # 0  4  8 12
    # 1  5  9 13
    # 2  6 10 14
    # 3  7 11 15
    data = list(range(16))
    # Expected output after shifting rows:
    # 0  5 10 15
    # 1  6 11 12
    # 2  7  8 13
    # 3  4  9 14
    expected = [0,5,10,15,1,6,11,12,2,7,8,13,3,4,9,14]
    assert shift_rows(data) == expected

def test_shift_rows_identity_for_zero_matrix():
    # All zeros should remain zeros after any shift
    data = [0] * 16
    assert shift_rows(data) == data

def test_shift_rows_invalid_length_raises():
    # shift_rows expects a 16-element list; shorter list triggers IndexError
    with pytest.raises(IndexError):
        shift_rows([1, 2, 3])  # too short
