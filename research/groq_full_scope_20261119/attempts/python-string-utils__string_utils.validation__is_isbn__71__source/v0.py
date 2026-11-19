import pytest
from string_utils.validation import is_isbn

def test_valid_isbn_13_with_normalization():
    # ISBN-13 with hyphens should be accepted when normalize=True
    isbn = "978-0-306-40615-7"
    assert is_isbn(isbn, normalize=True) is True

def test_valid_isbn_10_without_normalization():
    # ISBN-10 without hyphens should be accepted when normalize=False
    isbn = "0306406152"
    assert is_isbn(isbn, normalize=False) is True

def test_invalid_isbn_rejected():
    # Invalid ISBN (wrong checksum) should be rejected regardless of normalization
    isbn = "978-0-306-40615-8"  # checksum digit altered
    assert is_isbn(isbn, normalize=True) is False
