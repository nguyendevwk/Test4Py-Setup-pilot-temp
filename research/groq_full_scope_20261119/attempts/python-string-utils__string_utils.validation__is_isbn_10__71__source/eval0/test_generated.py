import pytest
from string_utils.validation import is_isbn_10

def test_valid_isbn_with_hyphens_and_normalization():
    # ISBN 10 with hyphens should be accepted when normalize=True
    isbn = "0-306-40615-2"
    assert is_isbn_10(isbn) is True
    # Same ISBN without hyphens should also be accepted
    assert is_isbn_10("0306406152") is True

def test_invalid_isbn_and_normalization_flag():
    # ISBN with hyphens but normalize=False should reject
    isbn = "0-306-40615-2"
    assert is_isbn_10(isbn, normalize=False) is False
    # Invalid checksum should reject regardless of normalization
    assert is_isbn_10("0-306-40615-3") is False

def test_error_on_non_string_input():
    # Passing a non-string should raise a TypeError or AttributeError
    with pytest.raises((TypeError, AttributeError)):
        is_isbn_10(1234567890)
