import pytest
from httpie.client import ensure_path_as_is

def test_path_replacement_basic():
    """Basic replacement of path component."""
    orig = "http://example.com/../path/"
    prepped = "http://example.com/actual/?q=1"
    result = ensure_path_as_is(orig, prepped)
    # The scheme, netloc, params, query, fragment should stay from prepped
    assert result.startswith("http://example.com/../path/")
    assert "?q=1" in result
    # Ensure the path is exactly the original path
    assert result.split("?")[0].endswith("/../path/")

def test_path_replacement_with_empty_path():
    """When original URL has an empty path, the result should have an empty path."""
    orig = "https://host"
    prepped = "https://host/some/thing?x=2"
    result = ensure_path_as_is(orig, prepped)
    # Path should be empty, query preserved
    assert result == "https://host?x=2"

def test_path_replacement_with_complex_components():
    """Ensure that other components (params, query, fragment) are preserved."""
    orig = "http://user:pass@host:8080/../path;param?orig=1#frag"
    prepped = "http://host:80/other?prepped=2#otherfrag"
    result = ensure_path_as_is(orig, prepped)
    # Scheme, netloc, params, query, fragment from prepped
    assert result.startswith("http://host:80/../path;param")
    assert "?prepped=2" in result
    assert "#otherfrag" in result
    # Path should be from orig
    assert result.split(";")[0].endswith("/../path")
