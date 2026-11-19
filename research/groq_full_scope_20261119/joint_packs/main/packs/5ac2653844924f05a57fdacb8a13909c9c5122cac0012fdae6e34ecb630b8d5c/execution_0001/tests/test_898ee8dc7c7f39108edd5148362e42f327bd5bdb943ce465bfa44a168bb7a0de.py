import pytest
from string_utils.validation import is_isbn_13

def test_valid_isbn_with_and_without_hyphens():
    # Valid ISBN-13 with no hyphens
    assert is_isbn_13('9780306406157') is True
    # Valid ISBN-13 with hyphens, normalization enabled
    assert is_isbn_13('978-0-306-40615-7') is True
    # Same string with normalization disabled should fail
    assert is_isbn_13('978-0-306-40615-7', normalize=False) is False

def test_invalid_isbn_due_to_wrong_checksum():
    # Alter last digit to break checksum
    assert is_isbn_13('9780306406158') is False

def test_non_string_input_raises_type_error():
    with pytest.raises(TypeError):
        is_isbn_13(9780306406157)  # passing an int instead of a string
