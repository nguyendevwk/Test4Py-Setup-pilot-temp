import pytest
from youtube_dl.aes import shift_rows_inv

def test_shift_rows_inv_known_pattern():
    # Input: sequential bytes 0..15
    data = list(range(16))
    result = shift_rows_inv(data)
    # Build expected result using the same mapping logic
    expected = []
    for column in range(4):
        for row in range(4):
            idx = ((column - row) & 0b11) * 4 + row
            expected.append(data[idx])
    assert result == expected
    # Ensure the result has the same length
    assert len(result) == 16

def test_shift_rows_inv_all_zeros():
    data = [0] * 16
    result = shift_rows_inv(data)
    assert result == [0] * 16
    assert len(result) == 16

def test_shift_rows_inv_invalid_length():
    # Too short input should raise IndexError during indexing
    data = list(range(15))
    with pytest.raises(IndexError):
        shift_rows_inv(data)
