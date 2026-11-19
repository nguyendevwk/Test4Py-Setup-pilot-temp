import pytest
from string_utils.generation import random_string

def test_random_string_length_and_charset():
    """Random string should have the requested length and only contain allowed characters."""
    size = 15
    result = random_string(size)
    assert isinstance(result, str)
    assert len(result) == size
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    assert set(result).issubset(allowed)

def test_random_string_minimum_size():
    """Calling with size=1 should return a single allowed character."""
    result = random_string(1)
    assert isinstance(result, str)
    assert len(result) == 1
    assert result[0] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def test_random_string_invalid_size_raises():
    """Non‑positive or non‑int size should raise ValueError."""
    with pytest.raises(ValueError):
        random_string(0)
    with pytest.raises(ValueError):
        random_string(-5)
    with pytest.raises(ValueError):
        random_string(3.14)
