import pytest
from httpie.client import ensure_path_as_is

def test_path_replacement_with_query_and_fragment():
    orig = "https://example.com/../path?foo=bar#section"
    prepped = "https://example.com/clean?baz=qux#frag"
    result = ensure_path_as_is(orig, prepped)
    # Path should come from orig, query and fragment from prepped
    assert result == "https://example.com/../path?baz=qux#frag"

def test_path_replacement_when_original_has_no_path():
    orig = "http://host"
    prepped = "http://host/abc?x=1"
    result = ensure_path_as_is(orig, prepped)
    # Original path is empty, so prepped path should be replaced with empty string
    assert result == "http://host?x=1"

def test_path_replacement_with_complex_original_path():
    orig = "https://host.com/a/b/../c/./d.html"
    prepped = "https://host.com/ignored?param=value"
    result = ensure_path_as_is(orig, prepped)
    # The path component should be exactly as in orig, including dot segments
    assert result == "https://host.com/a/b/../c/./d.html?param=value"
