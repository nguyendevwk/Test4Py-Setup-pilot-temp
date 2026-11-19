import pytest
from string_utils.validation import is_isbn_13

def test_valid_isbn_with_and_without_hyphens():
    # Valid ISBN-13 with hyphens
    assert is_isbn_13("978-0306406157") is True
    # Same ISBN without hyphens
    assert is_isbn_13("9780306406157") is True
    # When normalization is disabled, hyphens cause failure
    assert is_isbn_13("978-0306406157", normalize=False) is False

def test_invalid_isbn_checksum_and_length():
    # Incorrect checksum digit
    assert is_isbn_13("9780306406158") is False
    # Too short string
    assert is_isbn_13("978030640615") is False
    # Too long string
    assert is_isbn_13("97803064061577") is False

def test_non_string_input_raises_type_error():
    with pytest.raises(TypeError):
        is_isbn_13(9780306406157)  # passing int instead of str
