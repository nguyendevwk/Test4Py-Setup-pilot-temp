import pytest
from string_utils.validation import is_number
from string_utils.errors import InvalidInputError

def test_is_number_valid_cases():
    """Verify that valid numeric strings are accepted."""
    assert is_number("42") is True
    assert is_number("-9.12") is True
    assert is_number("+3.1415") is True
    assert is_number("1e3") is True
    assert is_number("-2E-5") is True
    # Edge case: leading/trailing whitespace should be considered invalid
    assert is_number(" 42") is False
    assert is_number("42 ") is False

def test_is_number_invalid_strings():
    """Verify that non‑numeric strings return False."""
    assert is_number("1 2 3") is False
    assert is_number("abc") is False
    assert is_number("") is False
    assert is_number("1.2.3") is False
    assert is_number("e10") is False

def test_is_number_invalid_type_raises():
    """Verify that passing a non‑string raises InvalidInputError."""
    with pytest.raises(InvalidInputError):
        is_number(42)          # int
    with pytest.raises(InvalidInputError):
        is_number(None)        # NoneType
    with pytest.raises(InvalidInputError):
        is_number([1, 2, 3])   # list
