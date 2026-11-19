import pytest
from string_utils.manipulation import slugify
from string_utils.errors import InvalidInputError

def test_slugify_behavior():
    # Basic slugification with default separator
    assert slugify('Top 10 Reasons To Love Dogs!!!') == 'top-10-reasons-to-love-dogs'
    # Custom separator
    assert slugify('Hello World', '_') == 'hello_world'
    # Non‑ASCII characters are transliterated
    assert slugify('Mönstér Mägnët') == 'monster-magnet'
    # Multiple spaces collapse into a single separator
    assert slugify('Hello   World') == 'hello-world'
    # Returned value is always a string
    assert isinstance(slugify('Test'), str)
    # Non‑string input raises InvalidInputError
    with pytest.raises(InvalidInputError):
        slugify(123)
