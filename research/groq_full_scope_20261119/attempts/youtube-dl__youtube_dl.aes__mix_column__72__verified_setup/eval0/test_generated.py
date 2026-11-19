import pytest
from youtube_dl.aes import mix_column

def test_mix_column_known_example():
    # Standard AES mix column matrix
    matrix = [
        [0x02, 0x03, 0x01, 0x01],
        [0x01, 0x02, 0x03, 0x01],
        [0x01, 0x01, 0x02, 0x03],
        [0x03, 0x01, 0x01, 0x02],
    ]
    data = [0x87, 0xF2, 0x4D, 0x97]
    expected = [0xFE, 0x6A, 0xE5, 0xF5]
    result = mix_column(data, matrix)
    assert result == expected, f"Expected {expected}, got {result}"

def test_mix_column_zero_and_all_ones():
    # Zero data with any matrix should yield zeros
    zero_matrix = [[0, 0, 0, 0] for _ in range(4)]
    zero_data = [0, 0, 0, 0]
    assert mix_column(zero_data, zero_matrix) == [0, 0, 0, 0]

    # All 0xFF data with matrix of all ones should yield all 0xFF
    ones_matrix = [[1, 1, 1, 1] for _ in range(4)]
    ff_data = [0xFF, 0xFF, 0xFF, 0xFF]
    assert mix_column(ff_data, ones_matrix) == [0xFF, 0xFF, 0xFF, 0xFF]

def test_mix_column_invalid_input():
    # Data list too short should raise IndexError
    matrix = [[1, 1, 1, 1] for _ in range(4)]
    short_data = [0x01, 0x02, 0x03]  # only 3 elements
    with pytest.raises(IndexError):
        mix_column(short_data, matrix)

    # Matrix row too short should raise IndexError
    bad_matrix = [[1, 1, 1] for _ in range(4)]  # each row has only 3 elements
    data = [0x01, 0x02, 0x03, 0x04]
    with pytest.raises(IndexError):
        mix_column(data, bad_matrix)
