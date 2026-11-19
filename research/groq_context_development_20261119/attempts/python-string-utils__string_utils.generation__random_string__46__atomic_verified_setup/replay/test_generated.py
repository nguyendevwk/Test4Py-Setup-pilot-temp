import string
import re
import pytest
from string_utils.generation import random_string

def test_random_string_length_and_charset():
    """Normal case: string length matches requested size and contains only allowed characters."""
    size = 12
    result = random_string(size)
    assert isinstance(result, str)
    assert len(result) == size
    allowed = set(string.ascii_letters + string.digits)
    assert set(result).issubset(allowed), "Result contains disallowed characters"

def test_random_string_boundary_minimum():
    """Boundary case: size=1 returns a single allowed character."""
    result = random_string(1)
    assert isinstance(result, str)
    assert len(result) == 1
    assert result[0] in string.ascii_letters + string.digits

def test_random_string_invalid_input_raises():
    """Error case: non-positive or non-integer size raises ValueError."""
    with pytest.raises(ValueError):
        random_string(0)
    with pytest.raises(ValueError):
        random_string(-5)
    with pytest.raises(ValueError):
        random_string(3.5)
    with pytest.raises(ValueError):
        random_string("10")
