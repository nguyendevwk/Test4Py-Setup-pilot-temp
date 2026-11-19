import pytest
from string_utils.validation import is_isbn, is_string
from string_utils.errors import InvalidInputError

def test_valid_isbn10_and_isbn13_with_normalization():
    # ISBN-10: 0-306-40615-2
    assert is_isbn("0306406152") is True
    assert is_isbn("0-306-40615-2") is True  # hyphens ignored by default
    # ISBN-13: 978-0-306-40615-7
    assert is_isbn("9780306406157") is True
    assert is_isbn("978-0-306-40615-7") is True

def test_invalid_input_and_normalize_flag():
    # Non-string input should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        is_isbn(1234567890)  # integer instead of string
    # When normalize=False, hyphens are not removed; string with hyphens fails
    assert is_isbn("978-0-306-40615-7", normalize=False) is False
    # But a pure digit string still passes
    assert is_isbn("9780306406157", normalize=False) is True

def test_boundary_cases_and_non_digit_characters():
    # Too short string
    assert is_isbn("123456789") is False
    # Too long string
    assert is_isbn("12345678901234") is False
    # Contains non-digit characters (except hyphen)
    assert is_isbn("97803064061a7") is False
    # Empty string
    assert is_isbn("") is False
