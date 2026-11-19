import pytest
from string_utils.manipulation import roman_encode
from string_utils.errors import InvalidInputError

def test_roman_encode_basic_numbers(tmp_path):
    # Basic conversion for a few numbers
    assert roman_encode(1) == "I"
    assert roman_encode(4) == "IV"
    assert roman_encode(9) == "IX"
    assert roman_encode(58) == "LVIII"
    assert roman_encode(1994) == "MCMXCIV"

def test_roman_encode_boundary_and_string_input(tmp_path):
    # Boundary values
    assert roman_encode(3999) == "MMMCMXCIX"
    # String input that represents a valid integer
    assert roman_encode("2020") == "MMXX"
    # Leading zeros should be handled correctly
    assert roman_encode("001") == "I"

def test_roman_encode_invalid_inputs(tmp_path):
    # Zero is invalid
    with pytest.raises(InvalidInputError):
        roman_encode(0)
    # Negative numbers are invalid
    with pytest.raises(InvalidInputError):
        roman_encode(-5)
    # Numbers above 3999 are invalid
    with pytest.raises(InvalidInputError):
        roman_encode(4000)
    # Non-numeric string is invalid
    with pytest.raises(InvalidInputError):
        roman_encode("abc")
    # Empty string is invalid
    with pytest.raises(InvalidInputError):
        roman_encode("")
