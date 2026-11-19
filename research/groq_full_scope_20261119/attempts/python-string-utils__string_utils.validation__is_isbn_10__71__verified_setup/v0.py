import pytest
from string_utils.validation import is_isbn_10
from string_utils.errors import InvalidInputError

def test_valid_isbn_10_with_and_without_hyphens():
    # Valid ISBN 10 with no hyphens
    assert is_isbn_10('1506715214') is True
    # Valid ISBN 10 with hyphens, default normalization
    assert is_isbn_10('150-6715214') is True
    # Same string with normalization disabled should be invalid
    assert is_isbn_10('150-6715214', normalize=False) is False

def test_invalid_isbn_10_due_to_wrong_checksum():
    # Alter last digit to break checksum
    assert is_isbn_10('1506715215') is False
    # Completely random string of digits
    assert is_isbn_10('1234567890') is False

def test_error_on_empty_input():
    # Empty string should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        is_isbn_10('')
