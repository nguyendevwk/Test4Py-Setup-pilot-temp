import pytest
from httpie.client import ensure_path_as_is

def test_path_replacement_basic():
    """Basic replacement of path component."""
    orig = "http://example.com/../path/"
    prepped = "http://example.com/actual?query=1#frag"
    result = ensure_path_as_is(orig, prepped)
    # Path should be replaced, other parts unchanged
    assert result == "http://example.com/../path/?query=1#frag"

def test_path_replacement_with_empty_and_query():
    """Ensure empty path from original is preserved."""
    orig = "https://host.com"
    prepped = "https://host.com/used?x=1"
    result = ensure_path_as_is(orig, prepped)
    # Original path is empty, so result should have no path component
    assert result == "https://host.com?x=1"

def test_path_replacement_with_invalid_url_raises():
    """urlparse accepts any string, but ensure_path_as_is should still work."""
    orig = "not a url"
    prepped = "http://valid.com/path"
    result = ensure_path_as_is(orig, prepped)
    # Since orig has no scheme, path is empty; result should keep prepped path
    assert result == "http://valid.com/path"
