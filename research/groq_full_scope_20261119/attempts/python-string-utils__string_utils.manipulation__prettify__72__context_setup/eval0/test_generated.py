import pytest
from string_utils.manipulation import prettify
from string_utils.errors import InvalidInputError

def test_prettify_basic_formatting():
    raw = "  hello,world!  this is a test. 100 %  of  success  "
    expected = "Hello, world! This is a test. 100% of success"
    assert prettify(raw) == expected

def test_prettify_quotes_and_brackets_and_genitive():
    raw = 'foo" bar"baz (qux )quux  "corge" grault  "garply"  "waldo"  "fred"  "plugh"  "xyzzy"  "thud"  '
    expected = 'Foo "bar" baz (qux) quux "corge" grault "garply" "waldo" "fred" "plugh" "xyzzy" "thud"'
    assert prettify(raw) == expected

def test_prettify_invalid_input_raises():
    with pytest.raises(InvalidInputError):
        prettify(123)  # non-string input should raise
