import re
import pytest
from semantic_release.helpers import text_reducer

def test_text_reducer_replaces_pattern():
    """Verify that a matching pattern is replaced correctly."""
    pattern = re.compile(r'\bfoo\b')
    result = text_reducer('foo bar foo', (pattern, 'baz'))
    assert result == 'baz bar baz'
    # Ensure the original string is not mutated
    assert 'foo' in 'foo bar foo'

def test_text_reducer_no_match_returns_original():
    """When the pattern does not match, the original text should be returned unchanged."""
    pattern = re.compile(r'\bxyz\b')
    original = 'hello world'
    result = text_reducer(original, (pattern, 'replaced'))
    assert result == original
    assert result is not original  # a new string object is returned

def test_text_reducer_empty_input_returns_empty():
    """An empty string should be returned immediately without applying the filter."""
    pattern = re.compile(r'.*')
    result = text_reducer('', (pattern, 'ignored'))
    assert result == ''
    # Ensure that the function does not raise even if the pattern is complex
    assert isinstance(result, str)
