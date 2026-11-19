import pytest
from string_utils.validation import is_isbn_13

def test_valid_isbn_with_hyphens():
    # ISBN 13 with hyphens should be accepted when normalize=True
    isbn = "978-0-306-40615-7"
    assert is_isbn_13(isbn) is True

def test_invalid_checksum():
    # Alter last digit to break checksum; should be rejected
    isbn = "978-0-306-40615-8"  # last digit changed from 7 to 8
    assert is_isbn_13(isbn) is False

def test_non_digit_characters_error():
    # ISBN containing letters should be rejected even with normalization
    isbn = "978-0-3A6-40615-7"
    assert is_isbn_13(isbn) is False
