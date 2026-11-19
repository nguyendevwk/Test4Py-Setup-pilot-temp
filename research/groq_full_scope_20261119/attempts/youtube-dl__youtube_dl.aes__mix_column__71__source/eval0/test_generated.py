import pytest
from youtube_dl.aes import mix_column

def test_mix_column_identity_matrix():
    # Identity matrix: each row has a single 1 on the diagonal
    identity_matrix = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]
    data = [1, 2, 3, 4]
    # With the identity matrix, each mixed value should be the xor of all data
    # because rijndael_mul(x,1) == x and xor is used.
    expected = [1 ^ 2 ^ 3 ^ 4] * 4  # 1^2^3^4 == 4
    assert mix_column(data, identity_matrix) == expected

def test_mix_column_all_ones_matrix():
    # Matrix of all ones: each mixed value is xor of all data elements
    ones_matrix = [[1] * 4 for _ in range(4)]
    data = [5, 9, 12, 7]
    # 5 ^ 9 ^ 12 ^ 7 == 5^9=12, 12^12=0, 0^7=7
    expected = [7] * 4
    assert mix_column(data, ones_matrix) == expected

def test_mix_column_invalid_data_length():
    # Data list shorter than required should raise IndexError
    matrix = [[1] * 4 for _ in range(4)]
    data = [1, 2, 3]  # only 3 elements
    with pytest.raises(IndexError):
        mix_column(data, matrix)
