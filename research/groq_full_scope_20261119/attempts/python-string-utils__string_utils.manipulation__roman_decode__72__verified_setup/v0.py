import pytest
from string_utils.manipulation import roman_decode
from string_utils.errors import InvalidInputError

def test_valid_roman_basic():
    # Basic Roman numerals
    assert roman_decode('I') == 1
    assert roman_decode('IV') == 4
    assert roman_decode('IX') == 9
    assert roman_decode('X') == 10
    assert roman_decode('XL') == 40
    assert roman_decode('L') == 50
    assert roman_decode('XC') == 90
    assert roman_decode('C') == 100
    assert roman_decode('CD') == 400
    assert roman_decode('D') == 500
    assert roman_decode('CM') == 900
    assert roman_decode('M') == 1000
    # Composite example
    assert roman_decode('MMXXI') == 2021

def test_valid_roman_boundary():
    # Test the maximum standard Roman numeral (3999)
    assert roman_decode('MMMCMXCIX') == 3999
    # Test a lower boundary (1)
    assert roman_decode('I') == 1

def test_invalid_roman_raises():
    # Invalid characters
    with pytest.raises(InvalidInputError):
        roman_decode('ABC')
    # Incorrect ordering
    with pytest.raises(InvalidInputError):
        roman_decode('IIV')
    # Empty string
    with pytest.raises(InvalidInputError):
        roman_decode('')
    # Lowercase input should be invalid
    with pytest.raises(InvalidInputError):
        roman_decode('vii')
