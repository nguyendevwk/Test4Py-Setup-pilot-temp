import pytest
from string_utils.manipulation import slugify
from string_utils.errors import InvalidInputError

def test_slugify_basic():
    """Slugify should convert a normal sentence into a lower‑case, hyphenated slug."""
    result = slugify('Top 10 Reasons To Love Dogs!!!')
    assert result == 'top-10-reasons-to-love-dogs'
    # Ensure no spaces or punctuation remain
    assert ' ' not in result
    assert all(c.isalnum() or c == '-' for c in result)

def test_slugify_unicode_and_separator():
    """Slugify should transliterate Unicode characters and use the supplied separator."""
    result = slugify('Mönstér Mägnët', separator='_')
    assert result == 'monster_magnet'
    # Verify that the separator is used correctly
    assert '_' in result
    assert '-' not in result

def test_slugify_invalid_input():
    """Slugify should raise InvalidInputError when the input is not a string."""
    with pytest.raises(InvalidInputError):
        slugify(12345)          # non‑string input
    with pytest.raises(InvalidInputError):
        slugify(None)           # non‑string input
