import pytest
from string_utils.manipulation import roman_decode
from string_utils.errors import InvalidInputError

def test_roman_decode_basic():
    """Normal case: simple Roman numeral."""
    assert roman_decode('VII') == 7

def test_roman_decode_boundary():
    """Boundary case: largest standard Roman numeral (3999)."""
    assert roman_decode('MMMCMXCIX') == 3999

def test_roman_decode_invalid():
    """Error case: invalid Roman numeral should raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        roman_decode('ABCD')
