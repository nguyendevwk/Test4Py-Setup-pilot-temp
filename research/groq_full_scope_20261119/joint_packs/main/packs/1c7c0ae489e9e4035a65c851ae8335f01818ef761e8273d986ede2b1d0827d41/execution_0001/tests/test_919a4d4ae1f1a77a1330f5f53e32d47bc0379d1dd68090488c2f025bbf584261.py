import pytest
from string_utils.manipulation import slugify
from string_utils.errors import InvalidInputError

def test_slugify_basic_normalization():
    # Normal case: spaces, punctuation, mixed case
    result = slugify('Top 10 Reasons To Love Dogs!!!')
    assert result == 'top-10-reasons-to-love-dogs'
    # Ensure separator can be changed
    result_dash = slugify('Hello World', separator='_')
    assert result_dash == 'hello_world'
    # Verify that non-alphanumeric characters are removed
    assert '!' not in result
    assert ' ' not in result

def test_slugify_unicode_and_duplicate_separators():
    # Unicode characters should be transliterated to ASCII
    result = slugify('Mönstér Mägnët')
    assert result == 'monster-magnet'
    # Multiple spaces or punctuation should collapse into a single separator
    result_multiple = slugify('  A   B__C  ', separator='-')
    assert result_multiple == 'a-b-c'
    # Leading/trailing separators should be trimmed
    assert not result_multiple.startswith('-')
    assert not result_multiple.endswith('-')

def test_slugify_invalid_input_raises_error():
    # Non-string input should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        slugify(12345)  # type: ignore[arg-type]
    with pytest.raises(InvalidInputError):
        slugify(None)  # type: ignore[arg-type]
    # Empty string is allowed but results in empty slug
    assert slugify('') == ''
