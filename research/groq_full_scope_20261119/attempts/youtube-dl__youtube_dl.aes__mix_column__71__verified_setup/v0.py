import pytest
from youtube_dl.aes import mix_column

def test_mix_column_identity_matrix():
    """When the matrix is the identity, mix_column should return the original data."""
    data = [1, 2, 3, 4]
    identity_matrix = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]
    result = mix_column(data, identity_matrix)
    assert result == data, f"Expected {data}, got {result}"

def test_mix_column_zero_matrix_and_data():
    """When both data and matrix contain only zeros, the result should be all zeros."""
    data = [0, 0, 0, 0]
    zero_matrix = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    result = mix_column(data, zero_matrix)
    assert result == [0, 0, 0, 0], f"Expected all zeros, got {result}"

def test_mix_column_invalid_data_length():
    """mix_column should raise an IndexError when data does not have length 4."""
    data = [1, 2, 3]  # too short
    matrix = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]
    with pytest.raises(IndexError):
        mix_column(data, matrix)
