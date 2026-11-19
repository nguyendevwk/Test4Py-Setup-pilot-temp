import pytest
import requests
from httpie.client import transform_headers, IGNORE_CONTENT_LENGTH_METHODS

def _prepare(method: str, url: str, headers: dict):
    """Helper to create a PreparedRequest from a Request."""
    req = requests.Request(method=method, url=url, headers=headers)
    session = requests.Session()
    return session.prepare_request(req)

def test_content_length_removed_when_misplaced():
    """When the request method is in IGNORE_CONTENT_LENGTH_METHODS and the
    prepared request has a misplaced 'Content-Length' of '0', it should be
    removed."""
    method = next(iter(IGNORE_CONTENT_LENGTH_METHODS))
    url = "http://example.com"
    # request has a non‑zero Content-Length, prepared has '0'
    request_headers = {"Content-Length": "123"}
    prepared_headers = {"Content-Length": "0", "User-Agent": "test"}
    prepared = _prepare(method, url, prepared_headers)
    # Apply transformation
    transform_headers(requests.Request(method=method, url=url, headers=request_headers),
                      prepared)
    # The header should be removed
    assert "Content-Length" not in prepared.headers
    # Other headers remain untouched
    assert prepared.headers["User-Agent"] == "test"

def test_content_length_not_removed_for_other_methods():
    """If the request method is not in IGNORE_CONTENT_LENGTH_METHODS, the
    'Content-Length' header should stay unchanged."""
    method = "GET"  # assume GET is not in IGNORE_CONTENT_LENGTH_METHODS
    url = "http://example.com"
    request_headers = {"Content-Length": "123"}
    prepared_headers = {"Content-Length": "0", "User-Agent": "test"}
    prepared = _prepare(method, url, prepared_headers)
    transform_headers(requests.Request(method=method, url=url, headers=request_headers),
                      prepared)
    # Header should still be present
    assert prepared.headers["Content-Length"] == "0"

def test_no_error_with_empty_headers():
    """transform_headers should handle empty headers without raising."""
    method = next(iter(IGNORE_CONTENT_LENGTH_METHODS))
    url = "http://example.com"
    request_headers = {}
    prepared_headers = {}
    prepared = _prepare(method, url, prepared_headers)
    # Should not raise any exception
    transform_headers(requests.Request(method=method, url=url, headers=request_headers),
                      prepared)
    # Headers remain empty
    assert prepared.headers == {}
