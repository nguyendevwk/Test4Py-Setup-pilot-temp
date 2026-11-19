import pytest
from string_utils.manipulation import slugify
from string_utils.errors import InvalidInputError

def test_slugify_basic_and_unicode():
    # Basic ASCII input
    assert slugify("Hello World") == "hello-world"
    # Unicode characters should be normalized to ASCII
    assert slugify("Mönstér Mägnët") == "monster-magnet"
    # Multiple separators and punctuation
    assert slugify("Python's 3.8+ features!!!") == "python-s-3-8-features"

def test_slugify_custom_separator_and_edge_cases(tmp_path):
    # Custom separator
    assert slugify("Test 123", separator="_") == "test_123"
    # Leading/trailing spaces and duplicate separators
    assert slugify("  Leading and trailing   ", separator="-") == "leading-and-trailing"
    # Empty string should return empty slug
    assert slugify("") == ""

def test_slugify_invalid_input():
    # Non-string input should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        slugify(12345)  # type: ignore[arg-type]
    with pytest.raises(InvalidInputError):
        slugify(None)  # type: ignore[arg-type]
