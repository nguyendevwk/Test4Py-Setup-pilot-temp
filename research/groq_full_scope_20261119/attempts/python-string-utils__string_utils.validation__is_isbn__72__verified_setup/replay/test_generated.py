import pytest
from string_utils.validation import is_isbn

def test_valid_isbn10_and_isbn13_with_normalization():
    # ISBN-10 with hyphens
    assert is_isbn("0-306-40615-2") is True
    # ISBN-13 with hyphens
    assert is_isbn("978-0-306-40615-7") is True
    # ISBN-13 without hyphens (normalize default True)
    assert is_isbn("9780306406157") is True
    # ISBN-10 without hyphens
    assert is_isbn("0306406152") is True

def test_invalid_isbn_and_normalize_flag():
    # Invalid checksum for ISBN-10
    assert is_isbn("0-306-40615-3") is False
    # Invalid length string
    assert is_isbn("12345") is False
    # Hyphens present but normalize=False should reject non‑digit string
    assert is_isbn("978-0-306-40615-7", normalize=False) is False
    # Hyphens absent but normalize=False should accept digit‑only ISBN
    assert is_isbn("9780306406157", normalize=False) is True

def test_type_error_on_non_string_input():
    with pytest.raises(TypeError):
        is_isbn(12345)  # passing an int instead of a string
