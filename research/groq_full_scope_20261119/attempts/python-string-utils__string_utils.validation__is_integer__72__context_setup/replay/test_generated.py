import pytest
from string_utils.validation import is_integer, is_number
from string_utils.errors import InvalidInputError

def test_is_integer_basic_cases():
    # Normal integer strings
    assert is_integer("0") is True
    assert is_integer("-123") is True
    assert is_integer("+456") is True
    # Scientific notation should be considered integer if no decimal point
    assert is_integer("1e3") is True
    # Non-integer numeric formats
    assert is_integer("42.0") is False
    assert is_integer("3.14") is False
    assert is_integer("1e-2") is False  # contains decimal point in exponent part
    # Non-numeric strings
    assert is_integer("abc") is False
    assert is_integer("") is False

def test_is_integer_boundary_and_edge_cases():
    # Very large integer
    large_int = "9" * 1000  # 1000-digit number
    assert is_integer(large_int) is True
    # Very small integer
    small_int = "-1"
    assert is_integer(small_int) is True
    # Scientific notation with large exponent
    sci_large = "1e308"
    assert is_integer(sci_large) is True
    # Scientific notation with negative exponent but no decimal point
    sci_negative = "1e-5"
    assert is_integer(sci_negative) is False  # contains decimal point in exponent part
    # String with leading/trailing spaces
    assert is_integer(" 42") is False
    assert is_integer("42 ") is False

def test_is_integer_invalid_input_type():
    # Passing non-string should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        is_integer(42)  # type: ignore[arg-type]
    with pytest.raises(InvalidInputError):
        is_integer(None)  # type: ignore[arg-type]
    # Ensure is_number also raises for non-string
    with pytest.raises(InvalidInputError):
        is_number(3.14)  # type: ignore[arg-type]
