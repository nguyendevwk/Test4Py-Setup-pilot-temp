import pytest
from httpie.client import ensure_path_as_is

def test_path_replacement_preserves_query_and_fragment():
    """
    Normal case: the function should replace only the path component
    while keeping query and fragment from the prepped URL.
    """
    orig = "http://example.com/../path/to/resource"
    prepped = "http://example.com/actual/path?foo=bar#section"
    result = ensure_path_as_is(orig, prepped)
    # The path should come from orig, query and fragment from prepped
    assert result == "http://example.com/../path/to/resource?foo=bar#section"

def test_path_replacement_with_empty_orig_path():
    """
    Boundary case: when the original URL has an empty path,
    the function should set the path to an empty string,
    effectively removing any path from the prepped URL.
    """
    orig = "http://example.com"
    prepped = "http://example.com/some/path?query=1"
    result = ensure_path_as_is(orig, prepped)
    # Path should be empty, query preserved
    assert result == "http://example.com?query=1"

def test_path_replacement_with_complex_prepped_url():
    """
    Error-like scenario: ensure that the function correctly handles
    a prepped URL that contains multiple slashes and a port number.
    """
    orig = "https://host.com/../new"
    prepped = "https://host.com:8080/old/path?x=1&y=2#frag"
    result = ensure_path_as_is(orig, prepped)
    # Path from orig, scheme, netloc, port, query, fragment from prepped
    assert result == "https://host.com:8080/../new?x=1&y=2#frag"
