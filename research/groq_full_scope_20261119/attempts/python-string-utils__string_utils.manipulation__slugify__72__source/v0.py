import pytest
from string_utils.manipulation import slugify
from string_utils.errors import InvalidInputError

def test_slugify_basic_and_normalization():
    # Basic example from docstring
    assert slugify('Top 10 Reasons To Love Dogs!!!') == 'top-10-reasons-to-love-dogs'
    # Unicode characters should be converted to ASCII equivalents
    assert slugify('Mönstér Mägnët') == 'monster-magnet'
    # Custom separator
    assert slugify('Hello World', separator='_') == 'hello_world'

def test_slugify_edge_cases_and_duplicates():
    # Leading/trailing spaces and multiple separators should be collapsed
    assert slugify('  Hello   World  ') == 'hello-world'
    # Consecutive non-alphanumeric characters should not create duplicate separators
    assert slugify('Hello---World!!!') == 'hello-world'
    # Empty string returns empty slug
    assert slugify('') == ''

def test_slugify_invalid_input_raises_error():
    # Non-string input should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        slugify(12345)  # type: ignore[arg-type]
    with pytest.raises(InvalidInputError):
        slugify(None)  # type: ignore[arg-type]
