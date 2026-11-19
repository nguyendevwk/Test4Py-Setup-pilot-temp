import time
import requests
from httpie.models import HTTPResponse

def create_response(status=200, reason='OK', headers=None, elapsed=0.0, raw_version=11):
    """Helper to create a minimal requests.Response with required attributes."""
    resp = requests.Response()
    resp.status_code = status
    resp.reason = reason
    resp._content = b''  # required for iter_content
    resp.headers = headers or {}
    resp.elapsed = time.timedelta(seconds=elapsed)
    # raw object with version attribute
    class Raw:
        def __init__(self, version):
            self.version = version
            self._original_response = None
    resp.raw = Raw(raw_version)
    # timestamp for metadata calculation
    resp._httpie_headers_parsed_at = time.monotonic()
    return resp

def test_headers_property_excludes_set_cookie_and_splits_cookies():
    resp = create_response(
        headers={
            'Content-Type': 'text/plain',
            'Set-Cookie': 'id=123; Path=/; HttpOnly, session=abc; Path=/',
            'X-Test': 'value'
        }
    )
    http_resp = HTTPResponse(resp)
    headers_str = http_resp.headers
    # status line present
    assert headers_str.startswith('HTTP/1.1 200 OK')
    # individual headers present
    assert 'Content-Type: text/plain' in headers_str
    assert 'X-Test: value' in headers_str
    # Set-Cookie header split into two lines
    assert 'Set-Cookie: id=123; Path=/; HttpOnly' in headers_str
    assert 'Set-Cookie: session=abc; Path=/' in headers_str
    # No raw Set-Cookie header line
    assert 'Set-Cookie: id=123; Path=/; HttpOnly, session=abc; Path=/' not in headers_str

def test_metadata_includes_elapsed_time_and_is_numeric():
    start = time.monotonic()
    resp = create_response(elapsed=0.123456)
    # simulate some delay after headers parsed
    time.sleep(0.05)
    http_resp = HTTPResponse(resp)
    meta = http_resp.metadata
    # metadata should contain a single line with elapsed time
    assert meta.startswith('Elapsed Time: ')
    elapsed_str = meta.split(': ')[1]
    # elapsed time should be a float string ending with 's'
    assert elapsed_str.endswith('s')
    elapsed_value = float(elapsed_str[:-1])
    # elapsed time should be at least the sum of elapsed and sleep
    assert elapsed_value >= 0.123456 + 0.05

def test_version_fallback_when_raw_missing():
    resp = create_response()
    # Remove raw to trigger fallback
    del resp.raw
    http_resp = HTTPResponse(resp)
    assert http_resp.version == '1.1'  # fallback to HTTP/1.1
