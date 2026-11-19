import pytest
from youtube_dl.aes import shift_rows

def test_shift_rows_basic():
    # 16-byte input where each byte is its index
    data = list(range(16))
    # Expected output computed manually
    expected = [
        0, 5,10,15,  # column 0 shifted by 0
        1, 6,11, 4,  # column 1 shifted by 1
        2, 7,12, 9,  # column 2 shifted by 2
        3, 8,13, 8   # column 3 shifted by 3
    ]
    # Note: the last element should be 8 (index 12) after shift
    expected = [0,5,10,15,1,6,11,4,2,7,12,9,3,8,13,8]
    assert shift_rows(data) == expected

def test_shift_rows_all_zeros():
    data = [0] * 16
    assert shift_rows(data) == [0] * 16

def test_shift_rows_invalid_length():
    # Provide fewer than 16 bytes; should raise IndexError
    data = [0] * 10
    with pytest.raises(IndexError):
        shift_rows(data)
