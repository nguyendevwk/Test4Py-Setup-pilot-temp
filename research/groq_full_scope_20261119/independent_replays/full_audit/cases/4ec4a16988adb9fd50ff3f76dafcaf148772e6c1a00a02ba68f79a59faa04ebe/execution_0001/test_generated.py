import re
import pytest
from semantic_release.helpers import text_reducer

def test_text_reducer_basic_replacement():
    """Verify that a simple pattern is replaced correctly."""
    pattern = re.compile(r"foo")
    result = text_reducer("foo bar foo", (pattern, "baz"))
    assert result == "baz bar baz"

def test_text_reducer_empty_input():
    """When the input text is empty, the function should return it unchanged."""
    pattern = re.compile(r".*")
    result = text_reducer("", (pattern, "ignored"))
    assert result == ""

def test_text_reducer_invalid_pattern_raises():
    """Passing an invalid pattern type should raise an AttributeError."""
    with pytest.raises(AttributeError):
        text_reducer("sample text", (None, "replacement"))
