import pytest
from string_utils.validation import is_isbn_10, InvalidInputError

def test_valid_isbn10_with_and_without_hyphens():
    # Valid ISBN-10 without hyphens
    assert is_isbn_10('1506715214') is True
    # Valid ISBN-10 with hyphens, default normalization
    assert is_isbn_10('150-6715214') is True
    # Same string with normalization disabled should fail
    assert is_isbn_10('150-6715214', normalize=False) is False

def test_boundary_case_invalid_length_and_non_digit():
    # Too short string
    assert is_isbn_10('123456789') is False
    # Too long string
    assert is_isbn_10('12345678901') is False
    # Contains non-digit characters (except hyphen)
    assert is_isbn_10('123456789X') is False

def test_invalid_input_type_raises_error():
    with pytest.raises(InvalidInputError):
        is_isbn_10(1234567890)  # non-string input should raise InvalidInputError
