import re
import pytest
from semantic_release.helpers import text_reducer

def test_text_reducer_replaces_pattern():
    """Verify that a compiled regex pattern replaces all occurrences."""
    pattern = re.compile(r'\bfoo\b')
    text = "foo bar foo baz"
    result = text_reducer(text, (pattern, "qux"))
    assert result == "qux bar qux baz"

def test_text_reducer_empty_input_returns_empty():
    """When the input text is empty, the function should return it unchanged."""
    pattern = re.compile(r'\w+')
    result = text_reducer("", (pattern, "x"))
    assert result == ""

def test_text_reducer_no_match_unchanged():
    """If the pattern does not match, the original text should be returned unchanged."""
    pattern = re.compile(r'\d+')
    text = "abc def"
    result = text_reducer(text, (pattern, "123"))
    assert result == text
