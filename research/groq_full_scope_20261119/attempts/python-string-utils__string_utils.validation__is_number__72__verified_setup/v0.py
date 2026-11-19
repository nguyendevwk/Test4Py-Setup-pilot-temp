import pytest
from string_utils.validation import is_number
from string_utils.errors import InvalidInputError

def test_is_number_valid_cases():
    """Verify that valid numeric strings return True."""
    valid_inputs = [
        "42",
        "19.99",
        "-9.12",
        "+7",
        "0",
        "-0.001",
        "1e3",
        "-2E-5",
        "+3.0e+10",
        "  5  ",  # whitespace should be considered invalid by regex
    ]
    # The last one should be False because of surrounding spaces
    for s in valid_inputs[:-1]:
        assert is_number(s) is True, f"Expected True for input {s!r}"
    # The string with spaces should be False
    assert is_number(valid_inputs[-1]) is False

def test_is_number_invalid_type_raises():
    """Passing a non‑string should raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        is_number(123)          # int
    with pytest.raises(InvalidInputError):
        is_number(None)         # NoneType
    with pytest.raises(InvalidInputError):
        is_number(["1", "2"])   # list

def test_is_number_edge_cases():
    """Test boundary numeric formats that are valid or invalid."""
    # Valid scientific notation with no exponent part
    assert is_number("1e0") is True
    # Valid with leading plus
    assert is_number("+1e-3") is True
    # Invalid: missing digits before exponent
    assert is_number("e10") is False
    # Invalid: exponent without digits
    assert is_number("1e") is False
    # Invalid: multiple decimal points
    assert is_number("1.2.3") is False
