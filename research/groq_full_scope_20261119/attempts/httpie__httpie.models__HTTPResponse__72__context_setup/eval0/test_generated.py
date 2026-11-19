import pytest
import requests
import time
from httpie.models import HTTPResponse, ELAPSED_TIME_LABEL
from urllib3.util import SKIP_HEADER, SKIPPABLE_HEADERS

def create_response(status=200, reason='OK', headers=None, body=b'', raw_version=11):
    """Helper to create a minimal requests.Response object."""
    resp = requests.Response()
    resp.status_code = status
    resp.reason = reason
    resp._content = body
    resp.headers = headers or {}
    resp.elapsed = time.timedelta(seconds=0.001)  # 1 ms
    # Mock raw object with version attribute
    class Raw:
        def __init__(self, version):
            self.version = version
            self._original_response = None
    resp.raw = Raw(raw_version)
    # Attach a timestamp for header parsing
    resp._httpie_headers_parsed_at = time.monotonic()
    return resp

def test_headers_property_excludes_and_splits_set_cookie():
    headers = {
        'Content-Type': 'text/plain',
        'Set-Cookie': 'id=123; Path=/; HttpOnly, session=abc; Path=/',
        'X-Custom': 'value'
    }
    resp = create_response(headers=headers)
    http_resp = HTTPResponse(resp)

    hdrs = http_resp.headers
    # Status line present
    assert hdrs.startswith('HTTP/1.1 200 OK')
    # Original headers except Set-Cookie
    assert 'Content-Type: text/plain' in hdrs
    assert 'X-Custom: value' in hdrs
    # Set-Cookie split into separate lines
    assert 'Set-Cookie: id=123' in hdrs
    assert 'Set-Cookie: Path=/' in hdrs
    assert 'Set-Cookie: HttpOnly' in hdrs
    assert 'Set-Cookie: session=abc' in hdrs
    assert 'Set-Cookie: Path=/' in hdrs
    # No duplicate Set-Cookie header line
    assert hdrs.count('Set-Cookie:') == 5

def test_metadata_includes_elapsed_time_label_and_value():
    resp = create_response()
    http_resp = HTTPResponse(resp)

    meta = http_resp.metadata
    # Should contain the elapsed time label
    assert ELAPSED_TIME_LABEL in meta
    # Extract the numeric value
    parts = meta.splitlines()
    label_line = next(p for p in parts if p.startswith(ELAPSED_TIME_LABEL))
    value_str = label_line.split(':', 1)[1].strip()
    # Value should end with 's'
    assert value_str.endswith('s')
    # Convert to float and ensure it's positive
    value = float(value_str.rstrip('s'))
    assert value > 0

def test_version_fallback_when_raw_missing():
    resp = create_response(raw_version=None)
    # Remove raw to trigger fallback
    del resp.raw
    http_resp = HTTPResponse(resp)
    assert http_resp.version == '1.1'
