import requests
import pytest
from httpie.cli.dicts import HTTPHeadersDict
from httpie.client import apply_missing_repeated_headers


def test_apply_missing_repeated_headers_restores_all_original_values(tmp_path):
    # Original headers contain the same header name twice with different values
    original = HTTPHeadersDict([("X-Test", "value1"), ("X-Test", "value2")])
    # Prepare a request that will override one of the values
    req = requests.Request("GET", "http://example.com")
    prepped = requests.Session().prepare_request(req)
    # Simulate that the request library has overridden the header to a single value
    prepped.headers["X-Test"] = "value1"
    # Apply the function
    apply_missing_repeated_headers(original, prepped)
    # After merging, both original values should be present
    assert prepped.headers.get_all("X-Test") == ["value1", "value2"]


def test_apply_missing_repeated_headers_preserves_overridden_value(tmp_path):
    # Original headers contain two values
    original = HTTPHeadersDict([("X-Override", "original1"), ("X-Override", "original2")])
    # Prepare a request that overrides the header to a new value
    req = requests.Request("GET", "http://example.com")
    prepped = requests.Session().prepare_request(req)
    prepped.headers["X-Override"] = "newvalue"
    # Apply the function
    apply_missing_repeated_headers(original, prepped)
    # The overridden value should remain, and original values should not be added
    assert prepped.headers.get_all("X-Override") == ["newvalue"]


def test_apply_missing_repeated_headers_no_change_when_header_absent(tmp_path):
    # Original headers contain a header not present in the prepared request
    original = HTTPHeadersDict([("X-Only", "onlyvalue")])
    req = requests.Request("GET", "http://example.com")
    prepped = requests.Session().prepare_request(req)
    # Apply the function
    apply_missing_repeated_headers(original, prepped)
    # Since the header was not in the prepared request, nothing should change
    assert "X-Only" not in prepped.headers
