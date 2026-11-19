import pytest
import requests
from httpie.client import transform_headers, apply_missing_repeated_headers, IGNORE_CONTENT_LENGTH_METHODS
from httpie.cli.dicts import HTTPHeadersDict

def test_remove_misplaced_content_length():
    # Prepare a request with method OPTIONS and a Content-Length header that should be removed
    req = requests.Request(
        method="OPTIONS",
        url="http://example.com",
        headers={"Content-Length": "123"}
    )
    session = requests.Session()
    prepared = session.prepare_request(req)

    # Simulate requests adding a Content-Length of 0 for OPTIONS
    prepared.headers["Content-Length"] = "0"

    transform_headers(req, prepared)

    # The header should be removed because the original had a different value
    assert "Content-Length" not in prepared.headers

def test_preserve_original_repeated_headers():
    # Original request has two identical header names with different values
    original_headers = HTTPHeadersDict([("X-Token", "first"), ("X-Token", "second")])
    req = requests.Request(
        method="GET",
        url="http://example.com",
        headers=original_headers
    )
    session = requests.Session()
    prepared = session.prepare_request(req)

    # Simulate a header override that removes one of the values
    prepared.headers.pop("X-Token", None)
    prepared.headers["X-Token"] = "first"

    apply_missing_repeated_headers(original_headers, prepared)

    # After applying, both original values should be present again
    values = prepared.headers.get_all("X-Token")
    assert set(values) == {"first", "second"}

def test_no_change_when_headers_match():
    # Original request has a single header
    original_headers = HTTPHeadersDict([("Accept", "application/json")])
    req = requests.Request(
        method="GET",
        url="http://example.com",
        headers=original_headers
    )
    session = requests.Session()
    prepared = session.prepare_request(req)

    # Prepare request should already have the same header
    assert prepared.headers["Accept"] == "application/json"

    apply_missing_repeated_headers(original_headers, prepared)

    # No modification should occur
    assert prepared.headers["Accept"] == "application/json"
