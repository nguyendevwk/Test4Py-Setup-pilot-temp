import pytest
from string_utils.validation import is_isbn, is_string
from string_utils.errors import InvalidInputError

def test_valid_isbn10_and_isbn13_with_normalization():
    # ISBN-10 example: 0-306-40615-2
    isbn10 = "0-306-40615-2"
    assert is_isbn(isbn10) is True
    # ISBN-13 example: 978-0-306-40615-7
    isbn13 = "978-0-306-40615-7"
    assert is_isbn(isbn13) is True

def test_invalid_input_type_raises_error():
    # Passing a non-string should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        is_isbn(12345)  # int instead of str

def test_normalization_flag_affects_result():
    # ISBN-13 with hyphens should pass when normalize=True
    isbn_with_hyphens = "978-0-306-40615-7"
    assert is_isbn(isbn_with_hyphens, normalize=True) is True
    # Same string should fail when normalize=False because hyphens are not digits
    assert is_isbn(isbn_with_hyphens, normalize=False) is False
