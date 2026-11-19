import pytest
from string_utils.manipulation import prettify

def test_basic_prettify_example():
    """Test the example provided in the docstring."""
    raw = " unprettified string ,, like this one,will be\"prettified\" .it\\' s awesome! "
    expected = "Unprettified string, like this one, will be \"prettified\". It's awesome!"
    assert prettify(raw) == expected

def test_quotes_parentheses_and_percentage():
    """Test handling of quotes, parentheses, percentage signs and spacing rules."""
    raw = 'foo(bar )baz"  qux" 100 %  +  5 '
    # Expected transformations:
    # - space before/after '(' and ')'
    # - no space before/after '%'
    # - one space around '+'
    # - quotes spaced correctly
    expected = 'foo (bar) baz "qux" 100% + 5'
    assert prettify(raw) == expected

def test_genitive_and_arithmetic_spacing():
    """Test correct genitive formatting and arithmetic operator spacing."""
    raw = "dave' s dog + 3 * 4!  hello   world."
    expected = "Dave's dog + 3 * 4! Hello world."
    assert prettify(raw) == expected
