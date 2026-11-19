import pytest
from string_utils.manipulation import prettify
from string_utils.errors import InvalidInputError

def test_prettify_basic():
    # Basic punctuation and capitalization
    raw = "  hello world!  this is a test.  "
    expected = "Hello world! This is a test."
    assert prettify(raw) == expected

def test_prettify_complex():
    # Quotes, parentheses, percentage, genitive, and operator spacing
    raw = 'foo" bar"baz (qux ) 100 %  + 5  Dave\' s dog'
    expected = 'Foo "bar" baz (qux) 100% + 5 Dave\'s dog'
    assert prettify(raw) == expected

def test_prettify_invalid_input():
    # Passing a non-string should raise a TypeError
    with pytest.raises(TypeError):
        prettify(123)
