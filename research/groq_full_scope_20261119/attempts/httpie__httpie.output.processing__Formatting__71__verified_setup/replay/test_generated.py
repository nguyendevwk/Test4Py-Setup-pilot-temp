import pytest
from httpie.output.processing import Formatting
from httpie.context import Environment

def test_format_headers_no_plugins(tmp_path):
    """When no formatter groups are enabled, headers are returned unchanged."""
    formatter = Formatting(groups=[], env=Environment())
    original = "Content-Type: application/json\nX-Custom: 123"
    result = formatter.format_headers(original)
    assert result == original, "Headers should be unchanged when no plugins are active"

def test_format_body_invalid_mime(tmp_path):
    """When MIME type is invalid, body is returned unchanged regardless of plugins."""
    formatter = Formatting(groups=[], env=Environment())
    body = '{"key":"value"}'
    invalid_mime = "invalid/mime"
    result = formatter.format_body(body, invalid_mime)
    assert result == body, "Body should be unchanged for invalid MIME types"

def test_format_metadata_no_plugins(tmp_path):
    """When no formatter groups are enabled, metadata is returned unchanged."""
    formatter = Formatting(groups=[], env=Environment())
    metadata = "Request: GET / HTTP/1.1\nResponse: 200 OK"
    result = formatter.format_metadata(metadata)
    assert result == metadata, "Metadata should be unchanged when no plugins are active"
