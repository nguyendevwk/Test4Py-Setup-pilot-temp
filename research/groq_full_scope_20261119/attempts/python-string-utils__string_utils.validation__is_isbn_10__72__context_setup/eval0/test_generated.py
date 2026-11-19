import pytest
from string_utils.validation import is_isbn_10, InvalidInputError

def test_valid_isbn10_with_hyphens():
    """A correctly formatted ISBN‑10 with hyphens should validate."""
    isbn = "0-306-40615-2"
    assert is_isbn_10(isbn) is True
    # Normalization off should reject the hyphenated form
    assert is_isbn_10(isbn, normalize=False) is False

def test_invalid_isbn10_wrong_checksum():
    """An ISBN‑10 with an incorrect checksum should be rejected."""
    # This is a known invalid ISBN‑10 (checksum fails)
    invalid_isbn = "0-306-40615-3"
    assert is_isbn_10(invalid_isbn) is False

def test_invalid_input_type_raises_error():
    """Passing a non‑string should raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        is_isbn_10(1234567890)  # integer input
