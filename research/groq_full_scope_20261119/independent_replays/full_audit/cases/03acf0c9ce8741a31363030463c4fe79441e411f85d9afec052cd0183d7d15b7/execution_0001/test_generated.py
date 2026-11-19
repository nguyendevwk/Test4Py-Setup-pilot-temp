import pytest
from string_utils.validation import is_isbn

def test_valid_isbn13_with_and_without_hyphens():
    # ISBN-13 with hyphens should be accepted when normalize=True
    isbn_with_hyphens = "978-0-306-40615-7"
    assert is_isbn(isbn_with_hyphens, normalize=True) is True

    # Same ISBN without hyphens should also be accepted
    isbn_without_hyphens = "9780306406157"
    assert is_isbn(isbn_without_hyphens, normalize=True) is True

    # When normalization is disabled, hyphens must be removed
    assert is_isbn(isbn_with_hyphens, normalize=False) is False

def test_valid_isbn10_and_checksum_variants():
    # Valid ISBN-10 without hyphens
    isbn10 = "0306406152"
    assert is_isbn(isbn10, normalize=True) is True

    # Valid ISBN-10 with hyphens
    isbn10_hyphens = "0-306-40615-2"
    assert is_isbn(isbn10_hyphens, normalize=True) is True

    # Invalid checksum for ISBN-10 should fail
    invalid_isbn10 = "0306406153"
    assert is_isbn(invalid_isbn10, normalize=True) is False

def test_invalid_inputs_and_edge_cases():
    # Non-digit characters (except hyphen) should cause failure
    assert is_isbn("978030640615X", normalize=True) is False

    # Too short string should fail
    assert is_isbn("123456789", normalize=True) is False

    # Empty string should fail
    assert is_isbn("", normalize=True) is False

    # Passing a non-string should raise a TypeError
    with pytest.raises(TypeError):
        is_isbn(1234567890123)  # type: ignore[arg-type]
