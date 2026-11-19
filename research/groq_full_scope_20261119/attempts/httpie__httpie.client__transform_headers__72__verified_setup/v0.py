import pytest
import requests

from httpie.client import transform_headers


def test_remove_misplaced_content_length(tmp_path):
    """
    Verify that a misplaced 'Content-Length' header is removed when the
    request method is one that should ignore it (e.g., GET) and the
    prepared request incorrectly contains 'Content-Length: 0'.
    """
    # Build a request with a non‑zero Content-Length
    req = requests.Request(
        method="GET",
        url="http://example.com",
        headers={"Content-Length": "123"},
    )
    prepared = req.prepare()
    # Simulate requests adding a misplaced Content-Length of 0
    prepared.headers["Content-Length"] = "0"

    # Apply the transformation
    transform_headers(req, prepared)

    # The misplaced header should be removed
    assert "Content-Length" not in prepared.headers
    # The original header should remain untouched
    assert req.headers["Content-Length"] == "123"


def test_apply_missing_repeated_headers(tmp_path):
    """
    Verify that headers present in the original request but missing from
    the prepared request are added during transformation.
    """
    # Original request has an Accept header
    req = requests.Request(
        method="POST",
        url="http://example.com",
        headers={"Accept": "application/json"},
    )
    prepared = req.prepare()
    # Ensure the prepared request initially lacks the Accept header
    assert "Accept" not in prepared.headers

    # Apply the transformation
    transform_headers(req, prepared)

    # The Accept header should now be present in the prepared request
    assert prepared.headers["Accept"] == "application/json"


def test_no_unintended_header_modification(tmp_path):
    """
    Ensure that headers unrelated to the transformation logic remain
    unchanged after calling transform_headers.
    """
    # Original request with multiple headers
    req = requests.Request(
        method="PUT",
        url="http://example.com",
        headers={
            "User-Agent": "test-agent",
            "X-Custom-Header": "value",
            "Content-Type": "application/json",
        },
    )
    prepared = req.prepare()

    # Capture original headers
    original_prepared_headers = dict(prepared.headers)

    # Apply the transformation
    transform_headers(req, prepared)

    # Headers that should not be modified must remain identical
    for key in ("User-Agent", "X-Custom-Header", "Content-Type"):
        assert prepared.headers[key] == original_prepared_headers[key]
