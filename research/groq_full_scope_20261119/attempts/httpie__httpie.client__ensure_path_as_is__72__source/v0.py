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
    # Path should be from original, query and fragment from prepped
    assert result == "https://example.com/../path?baz=qux#other"

def test_path_replacement_with_empty_path_and_no_query():
    """
    Boundary case: original URL has an empty path and no query.
    The function should still replace the path correctly.
    """
    original = "http://localhost"
    prepped = "http://localhost:8080/some/endpoint?param=value"
    result = ensure_path_as_is(original, prepped)
    # The path should be empty (i.e., '/'), query from prepped
    assert result == "http://localhost:8080/?param=value"

def test_path_replacement_with_complex_netloc_and_port():
    """
    Error-like scenario: ensure that the function correctly handles
    URLs with IPv6 addresses and custom ports.
    """
    original = "https://[2001:db8::1]/path/segment"
    prepped = "https://[2001:db8::1]:8443/other?x=y"
    result = ensure_path_as_is(original, prepped)
    # Path from original, query from prepped, port preserved
    assert result == "https://[2001:db8::1]:8443/path/segment?x=y"
