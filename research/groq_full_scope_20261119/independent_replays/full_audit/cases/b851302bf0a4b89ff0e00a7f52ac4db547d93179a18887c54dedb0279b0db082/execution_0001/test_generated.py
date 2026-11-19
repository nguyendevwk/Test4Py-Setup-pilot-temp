import pytest
from string_utils.manipulation import slugify
from string_utils.errors import InvalidInputError

def test_slugify_basic_and_normalization():
    # Normal sentence with punctuation and mixed case
    result = slugify('Top 10 Reasons To Love Dogs!!!')
    assert result == 'top-10-reasons-to-love-dogs'
    # Verify that all characters are lowercase and separator is '-'
    assert result.islower()
    assert '-' in result
    # Ensure no spaces or punctuation remain
    assert ' ' not in result
    assert all(c.isalnum() or c == '-' for c in result)

def test_slugify_unicode_and_custom_separator():
    # Unicode characters should be converted to ASCII equivalents
    result = slugify('Mönstér Mägnët', separator='_')
    assert result == 'monster_magnet'
    # Custom separator is used
    assert '_' in result
    assert '-' not in result
    # No duplicate separators
    assert '__' not in result

def test_slugify_invalid_input_raises_error():
    # Non-string input should raise InvalidInputError
    with pytest.raises(InvalidInputError):
        slugify(12345)  # integer input
    with pytest.raises(InvalidInputError):
        slugify(None)   # None input
