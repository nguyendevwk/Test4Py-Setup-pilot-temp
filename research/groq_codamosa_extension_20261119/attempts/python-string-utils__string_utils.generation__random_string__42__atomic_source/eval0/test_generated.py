import pytest
from string_utils.generation import random_string

def test_random_string_length_and_charset():
    """Verify that the returned string has the requested length and only contains allowed characters."""
    size = 12
    result = random_string(size)
    assert isinstance(result, str)
    assert len(result) == size
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    assert set(result).issubset(allowed)

def test_random_string_minimum_size():
    """Check that the function works correctly for the smallest valid size."""
    result = random_string(1)
    assert isinstance(result, str)
    assert len(result) == 1
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    assert set(result).issubset(allowed)

def test_random_string_invalid_size_raises_value_error():
    """Ensure that a ValueError is raised for non‑positive or non‑integer sizes."""
    with pytest.raises(ValueError):
        random_string(0)
    with pytest.raises(ValueError):
        random_string(-5)
    with pytest.raises(ValueError):
        random_string(3.5)
