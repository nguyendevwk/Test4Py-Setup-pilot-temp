import pytest
import requests
from httpie.client import transform_headers, apply_missing_repeated_headers
from httpie.cli.dicts import HTTPHeadersDict
from httpie.cli.constants import HTTP_OPTIONS

# Helper to prepare a request
def _prepare(request: requests.Request) -> requests.PreparedRequest:
    session = requests.Session()
    return session.prepare_request(request)

def test_content_length_removal():
    """When a GET request has a misplaced Content-Length of 0, it should be removed."""
    req = requests.Request(
        method="GET",
        url="http://example.com",
        headers={"Content-Length": "123"},
    )
    prepared = _prepare(req)
    # Simulate requests inserting a 0 Content-Length for GET
    prepared.headers["Content-Length"] = "0"
    transform_headers(req, prepared)
    assert "Content-Length" not in prepared.headers

def test_missing_repeated_headers_preserve_original():
    """Headers that appear multiple times should keep all original values."""
    original = HTTPHeadersDict(
        [
            ("X-Token", "first"),
            ("X-Token", "second"),
            ("X-Other", "value"),
        ]
    )
    req = requests.Request(
        method="POST",
        url="http://example.com",
        headers=original,
    )
    prepared = _prepare(req)
    # Simulate a header override by requests
    prepared.headers["X-Token"] = "override"
    apply_missing_repeated_headers(original, prepared)
    # All original X-Token values should be present
    assert prepared.headers.get_all("X-Token") == ["first", "second"]
    # X-Other should remain unchanged
    assert prepared.headers["X-Other"] == "value"

def test_apply_missing_repeated_headers_no_change_when_no_override():
    """If requests does not override any header, the prepared headers stay the same."""
    original = HTTPHeadersDict([("Accept", "application/json")])
    req = requests.Request(
        method="GET",
        url="http://example.com",
        headers=original,
    )
    prepared = _prepare(req)
    # No override occurs
    apply_missing_repeated_headers(original, prepared)
    assert prepared.headers["Accept"] == "application/json"
