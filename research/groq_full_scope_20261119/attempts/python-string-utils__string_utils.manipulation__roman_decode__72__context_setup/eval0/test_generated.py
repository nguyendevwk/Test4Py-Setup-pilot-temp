import pytest
from string_utils.manipulation import roman_decode
from string_utils.errors import InvalidInputError

def test_valid_roman_basic():
    """Test decoding of a simple Roman numeral."""
    assert roman_decode('VII') == 7
    assert roman_decode('IV') == 4
    assert roman_decode('MCMXCIV') == 1994

def test_valid_roman_boundary():
    """Test decoding of a large Roman numeral near typical limits."""
    # The largest standard Roman numeral using the common subtractive notation is 3999 (MMMCMXCIX)
    assert roman_decode('MMMCMXCIX') == 3999

def test_invalid_roman_raises_error():
    """Test that invalid Roman numerals raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        roman_decode('IIII')          # invalid repetition
    with pytest.raises(InvalidInputError):
        roman_decode('VX')            # invalid subtractive pair
    with pytest.raises(InvalidInputError):
        roman_decode('')              # empty string
