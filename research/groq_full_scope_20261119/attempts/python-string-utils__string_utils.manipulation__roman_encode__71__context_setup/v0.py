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

def test_roman_encode_boundary_values(tmp_path):
    # Boundary values: 1 and 3999
    assert roman_encode(1) == "I"
    assert roman_encode(3999) == "MMMCMXCIX"

def test_roman_encode_invalid_inputs(tmp_path):
    # Non‑positive numbers, out of range, and non‑numeric types should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        roman_encode(0)
    with pytest.raises(InvalidInputError):
        roman_encode(-5)
    with pytest.raises(InvalidInputError):
        roman_encode(4000)
    with pytest.raises(InvalidInputError):
        roman_encode("abc")
    with pytest.raises(InvalidInputError):
        roman_encode(3.14)
