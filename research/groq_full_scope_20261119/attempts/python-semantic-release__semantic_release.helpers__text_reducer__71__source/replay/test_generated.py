import re
import pytest
from semantic_release.helpers import text_reducer

def test_text_reducer_replaces_all_occurrences(tmp_path):
    # Pattern that matches the word "foo" case‑insensitively
    pattern = re.compile(r"foo", re.IGNORECASE)
    replacement = "bar"
    input_text = "Foo is not foo, but foofoo is foofoo."
    expected = "bar is not bar, but barbar is barbar."
    result = text_reducer(input_text, (pattern, replacement))
    assert result == expected
    # Ensure the original string was not mutated
    assert input_text == "Foo is not foo, but foofoo is foofoo."

def test_text_reducer_returns_empty_for_empty_input():
    pattern = re.compile(r".*")
    replacement = "x"
    # Empty string should be returned unchanged
    assert text_reducer("", (pattern, replacement)) == ""

def test_text_reducer_no_match_returns_original(tmp_path):
    pattern = re.compile(r"xyz")
    replacement = "123"
    input_text = "abcdefg"
    # No match, so the text should be unchanged
    result = text_reducer(input_text, (pattern, replacement))
    assert result == input_text
    # Verify that the replacement string was not inserted
    assert "123" not in result
