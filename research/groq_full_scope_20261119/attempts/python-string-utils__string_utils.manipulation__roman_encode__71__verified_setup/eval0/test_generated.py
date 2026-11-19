import pytest
from string_utils.manipulation import roman_encode
from string_utils.errors import InvalidInputError

def test_roman_encode_normal_cases(tmp_path):
    # Normal conversion of integers and numeric strings
    assert roman_encode(1) == "I"
    assert roman_encode(4) == "IV"
    assert roman_encode(9) == "IX"
    assert roman_encode(58) == "LVIII"
    assert roman_encode(1994) == "MCMXCIV"
    assert roman_encode("2020") == "MMXX"

def test_roman_encode_boundary_cases(tmp_path):
    # Boundary values: smallest and largest allowed numbers
    assert roman_encode(1) == "I"
    assert roman_encode(3999) == "MMMCMXCIX"

def test_roman_encode_invalid_inputs(tmp_path):
    # Inputs outside the allowed range or wrong type should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        roman_encode(0)          # zero is not allowed
    with pytest.raises(InvalidInputError):
        roman_encode(4000)       # above upper limit
    with pytest.raises(InvalidInputError):
        roman_encode(-5)         # negative number
    with pytest.raises(InvalidInputError):
        roman_encode("abc")      # non-numeric string
    with pytest.raises(InvalidInputError):
        roman_encode(3.14)       # float is not accepted
