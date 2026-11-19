import pytest
import requests
from httpie.client import transform_headers
from httpie.client import IGNORE_CONTENT_LENGTH_METHODS

def test_content_length_removal(tmp_path):
    # Create a request with a non‑zero Content-Length header
    req = requests.Request(
        method="GET",
        url="http://example.com",
        headers={"Content-Length": "123", "Accept": "*/*"}
    )
    # Prepare the request; requests will set Content-Length to 0 for GET
    prepared = req.prepare()
    # Ensure the prepared request initially has the misplaced header
    assert prepared.headers.get("Content-Length") == "0"
    # Apply the transformation
    transform_headers(req, prepared)
    # The Content-Length header should be removed
    assert "Content-Length" not in prepared.headers
    # Other headers should be preserved
    assert prepared.headers.get("Accept") == "*/*"

def test_no_removal_for_non_ignored_methods(tmp_path):
    # Use a method that is not in IGNORE_CONTENT_LENGTH_METHODS
    req = requests.Request(
        method="POST",
        url="http://example.com",
        headers={"Content-Length": "456", "Content-Type": "application/json"}
    )
    prepared = req.prepare()
    # requests sets Content-Length correctly for POST
    assert prepared.headers.get("Content-Length") == "456"
    # Apply the transformation
    transform_headers(req, prepared)
    # The header should remain unchanged
    assert prepared.headers.get("Content-Length") == "456"
    assert prepared.headers.get("Content-Type") == "application/json"

def test_missing_headers_are_added(tmp_path):
    # Request has a header that the prepared request lacks
    req = requests.Request(
        method="GET",
        url="http://example.com",
        headers={"X-Custom-Header": "value", "Accept": "application/json"}
    )
    prepared = req.prepare()
    # Remove Accept to simulate missing header
    prepared.headers.pop("Accept", None)
    # Ensure Accept is missing before transformation
    assert "Accept" not in prepared.headers
    # Apply the transformation
    transform_headers(req, prepared)
    # The missing header should now be present
    assert prepared.headers.get("X-Custom-Header") == "value"
    assert prepared.headers.get("Accept") == "application/json"
