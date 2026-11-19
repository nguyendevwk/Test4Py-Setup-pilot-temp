import pytest
from httpie.output.processing import Formatting, is_valid_mime
from httpie.context import Environment

def test_format_headers_pass_through(tmp_path):
    """When no formatter plugins are enabled, headers are returned unchanged."""
    # Use an empty group list to avoid loading any plugins
    formatter = Formatting(groups=[], env=Environment())
    raw_headers = "Content-Type: application/json\r\nX-Custom: 123"
    result = formatter.format_headers(raw_headers)
    assert result == raw_headers, "Headers should be unchanged when no plugins are active"

def test_format_body_no_change_on_invalid_mime(tmp_path):
    """Body should be returned unchanged if MIME type is not recognized."""
    formatter = Formatting(groups=[], env=Environment())
    body = '{"key":"value"}'
    invalid_mime = "invalid/mime"
    result = formatter.format_body(body, invalid_mime)
    assert result == body, "Body should be unchanged for invalid MIME types"

def test_format_metadata_pass_through(tmp_path):
    """Metadata should be returned unchanged when no plugins are enabled."""
    formatter = Formatting(groups=[], env=Environment())
    raw_metadata = "Request: GET / HTTP/1.1"
    result = formatter.format_metadata(raw_metadata)
    assert result == raw_metadata, "Metadata should be unchanged when no plugins are active"
