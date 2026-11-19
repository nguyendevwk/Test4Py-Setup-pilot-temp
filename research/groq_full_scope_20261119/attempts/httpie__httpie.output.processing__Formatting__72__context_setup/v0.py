import re
import pytest
from httpie.output.processing import Formatting, is_valid_mime, MIME_RE
from httpie.context import Environment

def test_formatting_with_no_plugins_returns_input():
    """When no formatter plugins are enabled, formatting methods should return the input unchanged."""
    formatter = Formatting(groups=[], env=Environment())
    headers = "Content-Type: application/json"
    body = '{"key":"value"}'
    metadata = "Request: GET /"

    assert formatter.format_headers(headers) == headers
    assert formatter.format_body(body, "application/json") == body
    assert formatter.format_metadata(metadata) == metadata

def test_format_body_skips_when_mime_invalid():
    """format_body should skip processing when the MIME type is invalid."""
    formatter = Formatting(groups=[], env=Environment())
    body = "raw data"
    invalid_mime = "invalidmime"  # does not match MIME_RE

    # Ensure is_valid_mime correctly identifies invalid MIME
    assert not is_valid_mime(invalid_mime)

    # format_body should return the original body unchanged
    assert formatter.format_body(body, invalid_mime) == body

def test_format_body_with_valid_mime_and_no_plugins():
    """When MIME is valid but no plugins are enabled, format_body should return the original content."""
    formatter = Formatting(groups=[], env=Environment())
    body = "sample text"
    valid_mime = "text/plain"

    # Ensure is_valid_mime correctly identifies valid MIME
    assert is_valid_mime(valid_mime)

    # format_body should return the original body unchanged
    assert formatter.format_body(body, valid_mime) == body
