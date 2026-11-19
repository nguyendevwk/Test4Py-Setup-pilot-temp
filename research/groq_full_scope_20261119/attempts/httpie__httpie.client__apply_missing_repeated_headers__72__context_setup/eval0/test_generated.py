import pytest
import requests
from httpie.cli.dicts import HTTPHeadersDict
from httpie.client import apply_missing_repeated_headers

def test_apply_missing_repeated_headers_preserves_original_when_no_override():
    # Original headers contain two repeated fields
    original = HTTPHeadersDict([("X-Token", "abc"), ("X-Token", "def")])
    # Prepared request has the same header values but only one instance
    req = requests.Request("GET", "http://example.com")
    prepped = req.prepare()
    prepped.headers.update({"X-Token": "abc"})
    # Apply merging
    apply_missing_repeated_headers(original, prepped)
    # After merging, both original values should be present
    assert prepped.headers.get_all("X-Token") == ["abc", "def"]

def test_apply_missing_repeated_headers_keeps_overridden_value():
    # Original headers contain two repeated fields
    original = HTTPHeadersDict([("X-Token", "abc"), ("X-Token", "def")])
    # Prepared request overrides one value
    req = requests.Request("GET", "http://example.com")
    prepped = req.prepare()
    prepped.headers.update({"X-Token": "xyz"})
    # Apply merging
    apply_missing_repeated_headers(original, prepped)
    # The overridden value should remain, original values should not be added
    assert prepped.headers.get_all("X-Token") == ["xyz"]

def test_apply_missing_repeated_headers_no_original_header():
    # Original headers do not contain the field
    original = HTTPHeadersDict([("Content-Type", "application/json")])
    # Prepared request has a different header
    req = requests.Request("GET", "http://example.com")
    prepped = req.prepare()
    prepped.headers.update({"X-Token": "abc"})
    # Apply merging
    apply_missing_repeated_headers(original, prepped)
    # The request headers should remain unchanged
    assert prepped.headers.get_all("X-Token") == ["abc"]
    assert prepped.headers.get_all("Content-Type") == []
