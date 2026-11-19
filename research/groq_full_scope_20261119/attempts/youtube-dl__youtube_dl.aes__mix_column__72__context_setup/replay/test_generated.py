import pytest
from youtube_dl.aes import mix_column

def test_mix_column_basic():
    # Simple test with identity-like matrix and data
    data = [0x01, 0x02, 0x03, 0x04]
    matrix = [
        [0x01, 0x00, 0x00, 0x00],
        [0x00, 0x01, 0x00, 0x00],
        [0x00, 0x00, 0x01, 0x00],
        [0x00, 0x00, 0x00, 0x01],
    ]
    result = mix_column(data, matrix)
    # With an identity matrix, each output should equal the corresponding input
    assert result == [0x01, 0x02, 0x03, 0x04]

def test_mix_column_zero_data():
    # All zero input should produce all zero output regardless of matrix
    data = [0x00, 0x00, 0x00, 0x00]
    matrix = [
        [0x02, 0x03, 0x01, 0x01],
        [0x01, 0x02, 0x03, 0x01],
        [0x01, 0x01, 0x02, 0x03],
        [0x03, 0x01, 0x01, 0x02],
    ]
    result = mix_column(data, matrix)
    assert result == [0x00, 0x00, 0x00, 0x00]

def test_mix_column_invalid_matrix():
    # Matrix with insufficient columns should raise an IndexError
    data = [0x01, 0x02, 0x03, 0x04]
    bad_matrix = [
        [0x01, 0x02],          # only two columns
        [0x03, 0x04],
        [0x05, 0x06],
        [0x07, 0x08],
    ]
    with pytest.raises(IndexError):
        mix_column(data, bad_matrix)
