import pytest
from string_utils.manipulation import roman_encode
from string_utils.errors import InvalidInputError

def test_roman_encode_basic_numbers():
    # Basic conversions for a few representative numbers
    assert roman_encode(1) == "I"
    assert roman_encode(4) == "IV"
    assert roman_encode(9) == "IX"
    assert roman_encode(58) == "LVIII"
    assert roman_encode(1994) == "MCMXCIV"

def test_roman_encode_boundary_and_string_input():
    # Boundary values and string input
    assert roman_encode(3999) == "MMMCMXCIX"
    # String representation of a valid integer
    assert roman_encode("2020") == "MMXX"

def test_roman_encode_invalid_inputs():
    # Zero, negative, and out-of-range numbers should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        roman_encode(0)
    with pytest.raises(InvalidInputError):
        roman_encode(-5)
    with pytest.raises(InvalidInputError):
        roman_encode(4000)
    # Non-numeric string should also raise
    with pytest.raises(InvalidInputError):
        roman_encode("abc")
