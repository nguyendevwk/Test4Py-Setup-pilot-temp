import pytest
from string_utils.validation import is_isbn_13

def test_valid_isbn_with_and_without_hyphens(tmp_path):
    """A correct ISBN‑13 should validate regardless of hyphen placement when normalize=True."""
    isbn = "978-0-306-40615-7"
    assert is_isbn_13(isbn) is True
    # Removing hyphens should still be valid
    assert is_isbn_13("9780306406157") is True
    # With normalize=False, hyphens must be absent
    assert is_isbn_13(isbn, normalize=False) is False

def test_invalid_checksum_and_length():
    """ISBNs with wrong checksum or incorrect length should be rejected."""
    # Wrong checksum (last digit altered)
    bad_checksum = "9780306406158"
    assert is_isbn_13(bad_checksum) is False
    # Too short
    short_isbn = "978030640615"
    assert is_isbn_13(short_isbn) is False
    # Too long
    long_isbn = "97803064061577"
    assert is_isbn_13(long_isbn) is False

def test_non_string_input_raises_type_error():
    """Passing a non‑string should raise a TypeError because the function expects a string."""
    with pytest.raises(TypeError):
        is_isbn_13(9780306406157)  # integer input
    with pytest.raises(TypeError):
        is_isbn_13(None)           # None input
