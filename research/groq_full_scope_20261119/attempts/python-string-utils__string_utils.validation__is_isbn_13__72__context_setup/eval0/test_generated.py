import pytest
from string_utils.validation import is_isbn_13, InvalidInputError

def test_valid_isbn13_with_and_without_hyphens():
    # ISBN 13 that is valid when hyphens are ignored
    isbn = "978-0-306-40615-7"
    assert is_isbn_13(isbn) is True          # default normalize=True
    assert is_isbn_13(isbn, normalize=False) is False  # hyphens must be removed

def test_boundary_case_invalid_length_and_non_digit():
    # ISBN 13 must be exactly 13 digits; any deviation fails
    short_isbn = "978030640615"   # 12 digits
    long_isbn  = "97803064061570" # 14 digits
    non_digit_isbn = "97803064061a7"  # contains a non-digit
    assert is_isbn_13(short_isbn) is False
    assert is_isbn_13(long_isbn) is False
    assert is_isbn_13(non_digit_isbn) is False

def test_invalid_input_type_raises_error():
    # Non-string input should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        is_isbn_13(9780306406157)  # integer instead of string
