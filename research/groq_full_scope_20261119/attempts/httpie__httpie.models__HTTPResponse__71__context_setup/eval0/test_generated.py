import time
import requests
from httpie.models import HTTPResponse, ELAPSED_TIME_LABEL


def create_response(status_code=200, reason='OK', headers=None, body=b'',
                    version=11, elapsed_seconds=0.1):
    """Helper to create a minimal requests.Response object."""
    resp = requests.Response()
    resp.status_code = status_code
    resp.reason = reason
    resp._content = body
    resp.headers = headers or {}
    resp.elapsed = time.timedelta(seconds=elapsed_seconds)
    # raw object with version attribute
    class Raw:
        def __init__(self, version):
            self.version = version
            self._original_response = None
    resp.raw = Raw(version)
    # simulate header parsing time
    resp._httpie_headers_parsed_at = time.monotonic() - elapsed_seconds
    return resp


def test_headers_property_excludes_set_cookie_and_splits_cookies(tmp_path):
    resp = create_response(
        headers={
            'Content-Type': 'text/plain',
            'Set-Cookie': 'id=123; Path=/; HttpOnly, theme=light; Path=/',
            'X-Custom': 'value'
        }
    )
    http_resp = HTTPResponse(resp)
    headers_str = http_resp.headers
    # Status line present
    assert headers_str.startswith('HTTP/1.1 200 OK')
    # Set-Cookie header split into two lines
    assert 'Set-Cookie: id=123; Path=/; HttpOnly' in headers_str
    assert 'Set-Cookie: theme=light; Path=/' in headers_str
    # Other headers present
    assert 'Content-Type: text/plain' in headers_str
    assert 'X-Custom: value' in headers_str
    # No raw Set-Cookie header line
    assert 'Set-Cookie: id=123; Path=/; HttpOnly, theme=light; Path=/' not in headers_str


def test_metadata_elapsed_time(tmp_path):
    start = time.monotonic()
    resp = create_response(elapsed_seconds=0.05)
    http_resp = HTTPResponse(resp)
    # Wait a bit to ensure monotonic difference
    time.sleep(0.01)
    meta = http_resp.metadata
    # Metadata should contain the elapsed time label
    assert ELAPSED_TIME_LABEL in meta
    # Extract the numeric part
    elapsed_str = meta.splitlines()[0].split(': ')[1]
    elapsed_val = float(elapsed_str.rstrip('s'))
    # The elapsed time should be at least the sum of elapsed_seconds and the
    # time since headers were parsed (which is the sleep we did)
    assert elapsed_val >= 0.05 + 0.01
    # The value should be formatted with up to 10 decimal places
    assert len(elapsed_str.split('.')[1]) <= 10


def test_version_mapping_and_fallback(tmp_path):
    # HTTP/1.1
    resp1 = create_response(version=11)
    http_resp1 = HTTPResponse(resp1)
    assert http_resp1.version == '1.1'
    # HTTP/2.0
    resp2 = create_response(version=20)
    http_resp2 = HTTPResponse(resp2)
    assert http_resp2.version == '2.0'
    # Missing version attribute triggers fallback to 1.1
    class RawMissing:
        def __init__(self):
            self._original_response = None
    resp3 = create_response()
    resp3.raw = RawMissing()
    http_resp3 = HTTPResponse(resp3)
    assert http_resp3.version == '1.1'
