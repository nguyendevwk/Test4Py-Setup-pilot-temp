import pytest
from string_utils.validation import is_number
from string_utils.errors import InvalidInputError


def test_is_number_valid_examples():
    """Verify that typical numeric strings are accepted."""
    valid_cases = [
        "42",
        "19.99",
        "-9.12",
        "+7",
        "0",
        "-0.001",
        "1e3",
        "-2E-5",
        "+3.14e+10",
        "  5  ",  # whitespace should be considered invalid
    ]
    # The last case should be False because of surrounding spaces
    for s in valid_cases[:-1]:
        assert is_number(s) is True, f"Expected True for {s!r}"
    # The string with spaces is not a valid number
    assert is_number(valid_cases[-1]) is False


def test_is_number_boundary_and_edge_cases():
    """Test boundary conditions and edge numeric formats."""
    # Empty string
    assert is_number("") is False
    # Only sign
    assert is_number("+") is False
    assert is_number("-") is False
    # Sign with exponent but no mantissa
    assert is_number("e10") is False
    # Exponent without exponent part
    assert is_number("1e") is False
    # Decimal point without digits
    assert is_number(".") is False
    # Leading zeros
    assert is_number("000123") is True
    # Large exponent
    assert is_number("1e308") is True
    # Negative exponent
    assert is_number("1e-308") is True
    # Mixed case exponent
    assert is_number("1E+10") is True


def test_is_number_invalid_input_type():
    """Ensure that non-string inputs raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        is_number(123)          # int
    with pytest.raises(InvalidInputError):
        is_number(12.34)        # float
    with pytest.raises(InvalidInputError):
        is_number(None)         # NoneType
    with pytest.raises(InvalidInputError):
        is_number(['1', '2'])   # list
