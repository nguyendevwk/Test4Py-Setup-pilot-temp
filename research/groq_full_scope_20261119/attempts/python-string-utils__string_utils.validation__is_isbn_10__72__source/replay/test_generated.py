import pytest
from string_utils.validation import is_isbn_10

def test_valid_isbn_with_hyphens():
    # A known valid ISBN‑10 with hyphens
    isbn = "0-306-40615-2"
    assert is_isbn_10(isbn) is True
    # Normalization should ignore hyphens
    assert is_isbn_10(isbn, normalize=True) is True

def test_valid_isbn_without_hyphens_and_normalization_off():
    # Same ISBN without hyphens
    isbn = "0306406152"
    assert is_isbn_10(isbn) is True
    # When normalization is disabled, hyphens are not ignored
    assert is_isbn_10(isbn, normalize=False) is True

def test_invalid_isbn_and_wrong_format():
    # Incorrect checksum
    bad_isbn = "0-306-40615-3"
    assert is_isbn_10(bad_isbn) is False
    # Non‑digit characters (except hyphen)
    assert is_isbn_10("0-306-4061A-2") is False
    # Too short string
    assert is_isbn_10("123456789") is False
