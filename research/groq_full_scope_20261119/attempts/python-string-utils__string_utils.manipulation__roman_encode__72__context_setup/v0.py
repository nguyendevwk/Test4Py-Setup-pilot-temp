import pytest
from string_utils.manipulation import roman_encode
from string_utils.errors import InvalidInputError

def test_roman_encode_basic_numbers():
    # Basic conversions
    assert roman_encode(1) == "I"
    assert roman_encode(4) == "IV"
    assert roman_encode(9) == "IX"
    assert roman_encode(58) == "LVIII"
    assert roman_encode(1994) == "MCMXCIV"

def test_roman_encode_boundary_values():
    # Boundary values: smallest and largest allowed
    assert roman_encode(1) == "I"
    assert roman_encode(3999) == "MMMCMXCIX"

def test_roman_encode_invalid_inputs():
    # Values outside the allowed range or wrong types should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        roman_encode(0)          # zero is not allowed
    with pytest.raises(InvalidInputError):
        roman_encode(-5)         # negative numbers are invalid
    with pytest.raises(InvalidInputError):
        roman_encode(4000)       # exceeds upper bound
    with pytest.raises(InvalidInputError):
        roman_encode("abc")      # non-numeric string
    with pytest.raises(InvalidInputError):
        roman_encode(3.14)       # float is not an integer
