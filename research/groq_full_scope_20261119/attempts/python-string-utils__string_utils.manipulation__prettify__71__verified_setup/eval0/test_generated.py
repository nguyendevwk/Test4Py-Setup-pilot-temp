import pytest
from string_utils.manipulation import prettify
from string_utils.errors import InvalidInputError

def test_prettify_basic_formatting():
    raw = "  unprettified string ,, like this one,will be\"prettified\" .it\\' s awesome!  "
    expected = "Unprettified string, like this one, will be \"prettified\". It's awesome!"
    assert prettify(raw) == expected

def test_prettify_edge_cases():
    # Empty string should return empty string
    assert prettify("") == ""
    # String with only spaces should be trimmed to empty
    assert prettify("   ") == ""
    # String with punctuation and operators
    raw = "a+b  =c  d*e"
    expected = "A + b = c d * e"
    assert prettify(raw) == expected

def test_prettify_invalid_input():
    # Passing a non-string should raise an error
    with pytest.raises((TypeError, InvalidInputError)):
        prettify(None)
