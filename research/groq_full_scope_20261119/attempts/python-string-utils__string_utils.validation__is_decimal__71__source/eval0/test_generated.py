import pytest
from string_utils.validation import is_decimal

def test_is_decimal_true_for_standard_decimal():
    """A plain decimal string should return True."""
    assert is_decimal("42.0") is True

def test_is_decimal_false_for_integer_without_dot():
    """An integer string without a decimal point should return False."""
    assert is_decimal("42") is False

def test_is_decimal_raises_type_error_for_non_string():
    """Passing a non-string should raise a TypeError."""
    with pytest.raises(TypeError):
        is_decimal(42)  # type: ignore[arg-type]
