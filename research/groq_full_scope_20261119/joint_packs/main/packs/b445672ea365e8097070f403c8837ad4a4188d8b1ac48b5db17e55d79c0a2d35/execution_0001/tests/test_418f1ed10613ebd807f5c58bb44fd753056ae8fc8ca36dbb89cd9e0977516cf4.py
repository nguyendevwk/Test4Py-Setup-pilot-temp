import re
import pytest
from semantic_release.helpers import text_reducer

def test_text_reducer_basic_replacement():
    """Verify that a simple pattern is replaced correctly."""
    pattern = re.compile(r"foo")
    result = text_reducer("foo bar foo", (pattern, "baz"))
    assert result == "baz bar baz"

def test_text_reducer_no_match_and_empty_input():
    """When the pattern matches nothing or the input is empty, the original text is returned."""
    pattern = re.compile(r"xyz")
    # No match
    assert text_reducer("hello world", (pattern, "oops")) == "hello world"
    # Empty input
    assert text_reducer("", (pattern, "oops")) == ""

def test_text_reducer_invalid_filter_pair_type():
    """Passing a non‑Pattern object should raise an AttributeError because .sub is missing."""
    with pytest.raises(AttributeError):
        text_reducer("sample text", ("not a pattern", "replacement"))
