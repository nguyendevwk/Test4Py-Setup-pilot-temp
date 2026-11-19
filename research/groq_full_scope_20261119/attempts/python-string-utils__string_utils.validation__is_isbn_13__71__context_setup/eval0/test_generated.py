import pytest
from string_utils.validation import is_isbn_13
from string_utils.errors import InvalidInputError

def test_valid_isbn_with_hyphens():
    """ISBN 13 with hyphens should be accepted when normalize=True."""
    isbn = "978-0-306-40615-7"
    assert is_isbn_13(isbn) is True

def test_invalid_isbn_due_to_checksum():
    """ISBN 13 with incorrect checksum should be rejected."""
    isbn = "978-0-306-40615-8"  # last digit changed to break checksum
    assert is_isbn_13(isbn) is False

def test_non_string_input_raises_error():
    """Passing a non-string should raise InvalidInputError."""
    with pytest.raises(InvalidInputError):
        is_isbn_13(1234567890123)
