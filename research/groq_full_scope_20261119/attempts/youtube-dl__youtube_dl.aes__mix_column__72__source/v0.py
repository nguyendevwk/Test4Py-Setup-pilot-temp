import pytest
from youtube_dl.aes import mix_column

def test_mix_column_standard_matrix():
    # Standard AES mix column matrix
    matrix = [
        [2, 3, 1, 1],
        [1, 2, 3, 1],
        [1, 1, 2, 3],
        [3, 1, 1, 2],
    ]
    # Example from the AES specification
    data = [0x87, 0xF2, 0x4D, 0x97]
    expected = [0x47, 0x58, 0x30, 0xF1]
    result = mix_column(data, matrix)
    assert result == expected, f"Expected {expected}, got {result}"

def test_mix_column_all_ones_matrix():
    # Matrix with all ones: each output byte is XOR of all input bytes
    matrix = [[1, 1, 1, 1] for _ in range(4)]
    data = [0x01, 0x02, 0x04, 0x08]
    xor_all = 0x01 ^ 0x02 ^ 0x04 ^ 0x08
    expected = [xor_all, xor_all, xor_all, xor_all]
    result = mix_column(data, matrix)
    assert result == expected, f"Expected {expected}, got {result}"

def test_mix_column_invalid_data_length():
    # Data list shorter than 4 elements should raise IndexError
    matrix = [[1, 1, 1, 1] for _ in range(4)]
    data = [0x01, 0x02]  # too short
    with pytest.raises(IndexError):
        mix_column(data, matrix)
