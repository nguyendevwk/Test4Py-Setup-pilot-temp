import pytest
from string_utils.manipulation import slugify
from string_utils.errors import InvalidInputError

def test_slugify_basic_and_unicode():
    # Basic ASCII input
    assert slugify("Hello World") == "hello-world"
    # Unicode characters should be normalized to ASCII
    assert slugify("Mönstér Mägnët") == "monster-magnet"
    # Multiple separators and punctuation
    assert slugify("Python---is!! awesome") == "python-is-awesome"

def test_slugify_custom_separator_and_edge_cases(tmp_path):
    # Custom separator
    assert slugify("Python is great", separator="__") == "python__is__great"
    # Leading/trailing spaces and punctuation
    assert slugify("  Leading and trailing!  ") == "leading-and-trailing"
    # Empty string after stripping non-alphanumerics
    assert slugify("!!!") == ""

def test_slugify_invalid_input():
    # Non-string input should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        slugify(12345)  # type: ignore[arg-type]
    with pytest.raises(InvalidInputError):
        slugify(None)  # type: ignore[arg-type]
