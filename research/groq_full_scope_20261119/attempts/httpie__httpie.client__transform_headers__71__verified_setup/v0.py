import requests
import pytest
from httpie.client import transform_headers
from httpie.client import IGNORE_CONTENT_LENGTH_METHODS

def test_remove_misplaced_content_length(tmp_path):
    # Prepare a request with a non-zero Content-Length header
    req = requests.Request(
        method="POST",
        url="http://example.com",
        headers={"Content-Length": "123"},
        data="{}"
    )
    prepared = req.prepare()
    # Simulate requests inserting a zero Content-Length for POST
    prepared.headers["Content-Length"] = "0"
    # Apply transformation
    transform_headers(req, prepared)
    # The zero Content-Length should be removed
    assert "Content-Length" not in prepared.headers

def test_preserve_content_length_when_not_ignored(tmp_path):
    # Method not in IGNORE_CONTENT_LENGTH_METHODS
    req = requests.Request(
        method="GET",
        url="http://example.com",
        headers={"Content-Length": "456"},
        data="{}"
    )
    prepared = req.prepare()
    # Simulate requests inserting a zero Content-Length for GET
    prepared.headers["Content-Length"] = "0"
    # Apply transformation
    transform_headers(req, prepared)
    # The zero Content-Length should remain because GET is not ignored
    assert prepared.headers["Content-Length"] == "0"

def test_headers_from_request_are_copied(tmp_path):
    # Request has custom header that should be present in prepared request
    req = requests.Request(
        method="PUT",
        url="http://example.com",
        headers={"X-Custom-Header": "value"},
        data="{}"
    )
    prepared = req.prepare()
    # Apply transformation
    transform_headers(req, prepared)
    # The custom header should be present
    assert prepared.headers.get("X-Custom-Header") == "value"
