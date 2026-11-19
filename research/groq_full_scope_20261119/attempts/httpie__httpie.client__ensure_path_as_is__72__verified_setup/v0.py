import pytest
from httpie.client import ensure_path_as_is

def test_path_replacement_preserves_query_and_fragment():
    """
    Normal case: the function should replace only the path component,
    leaving query and fragment untouched.
    """
    original = "https://example.com/../path?foo=bar#section"
    prepped = "https://example.com/actual?baz=qux#other"
    result = ensure_path_as_is(original, prepped)
    # The path should come from the original URL
    assert result.startswith("https://example.com/../path")
    # Query and fragment should be preserved from the prepped URL
    assert "?baz=qux" in result
    assert "#other" in result
    # No other parts should be altered
    assert result == "https://example.com/../path?baz=qux#other"

def test_empty_path_in_original_keeps_prepped_path():
    """
    Boundary case: if the original URL has an empty path, the function
    should keep the prepped URL's path unchanged.
    """
    original = "http://host"
    prepped = "http://host/some/path?query=1"
    result = ensure_path_as_is(original, prepped)
    # Since original.path is empty, the prepped path should remain
    assert result == "http://host/some/path?query=1"

def test_path_with_trailing_slash_and_no_query():
    """
    Edge case: original URL has a trailing slash and no query,
    prepped URL has a different path and no query.
    """
    original = "https://example.org/dir/"
    prepped = "https://example.org/other"
    result = ensure_path_as_is(original, prepped)
    # The resulting URL should have the original path with trailing slash
    assert result == "https://example.org/dir/"
