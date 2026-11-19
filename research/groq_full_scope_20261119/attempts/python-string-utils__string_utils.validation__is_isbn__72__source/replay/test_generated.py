import pytest
from string_utils.validation import is_isbn

def test_valid_isbn13_with_hyphens_and_normalization():
    # ISBN-13 with hyphens should be accepted when normalize=True
    isbn = "978-0-306-40615-7"
    assert is_isbn(isbn, normalize=True) is True

def test_invalid_isbn_and_normalization_off():
    # Invalid ISBN should return False; disabling normalization requires digits only
    isbn = "978-0-306-40615-7"
    assert is_isbn(isbn, normalize=False) is False
    # Completely invalid string
    assert is_isbn("12345", normalize=True) is False

def test_valid_isbn10_without_hyphens_and_normalization_off():
    # ISBN-10 without hyphens should be accepted when normalize=False
    isbn = "0306406152"
    assert is_isbn(isbn, normalize=False) is True
