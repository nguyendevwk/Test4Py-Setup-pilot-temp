import pytest
from string_utils.validation import is_decimal
from string_utils.errors import InvalidInputError

def test_is_decimal_with_simple_decimal():
    """A plain decimal string should return True."""
    assert is_decimal("3.14") is True

def test_is_decimal_with_no_decimal_point():
    """A numeric string without a decimal point should return False."""
    assert is_decimal("42") is False

def test_is_decimal_with_invalid_input_type():
    """Passing a non‑string should raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        is_decimal(42)  # type: ignore[arg-type]
