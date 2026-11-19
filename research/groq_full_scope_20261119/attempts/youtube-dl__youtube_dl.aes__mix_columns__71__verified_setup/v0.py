import pytest
from youtube_dl.aes import mix_columns

def test_mix_columns_zero_input():
    """mix_columns should return all zeros when input is all zeros."""
    data = [0] * 16
    result = mix_columns(data)
    assert result == [0] * 16
    assert len(result) == 16
    assert all(isinstance(x, int) and 0 <= x <= 255 for x in result)

def test_mix_columns_length_and_range():
    """mix_columns should return a list of 16 integers each in 0-255."""
    data = list(range(16))
    result = mix_columns(data)
    assert isinstance(result, list)
    assert len(result) == 16
    assert all(isinstance(x, int) and 0 <= x <= 255 for x in result)

def test_mix_columns_invalid_length():
    """mix_columns should raise a ValueError when input length is not 16."""
    data = [0] * 12  # too short
    with pytest.raises(ValueError):
        mix_columns(data)
