import time
import requests
from httpie.models import HTTPResponse
from urllib3.util import SKIP_HEADER, SKIPPABLE_HEADERS
from httpie.utils import split_cookies

def create_response(status=200, headers=None, body=b''):
    """Helper to create a minimal requests.Response object."""
    resp = requests.Response()
    resp.status_code = status
    resp._content = body
    resp.headers = headers or {}
    resp.url = 'http://example.com'
    # simulate elapsed time
    resp.elapsed = time.timedelta(seconds=0.01)
    # simulate internal timestamp for metadata
    resp._httpie_headers_parsed_at = time.monotonic()
    return resp

def test_headers_property_excludes_set_cookie_and_splits_cookies():
    resp = create_response(
        headers={
            'Content-Type': 'text/plain',
            'Set-Cookie': 'id=123; Path=/; HttpOnly, session=abc; Path=/'
        }
    )
    http_resp = HTTPResponse(resp)
    headers_str = http_resp.headers
    # Status line should be first
    assert headers_str.startswith('HTTP/1.1 200 OK')
    # Content-Type header should be present
    assert 'Content-Type: text/plain' in headers_str
    # Set-Cookie header should be split into two lines
    assert headers_str.count('Set-Cookie:') == 2
    assert 'Set-Cookie: id=123; Path=/; HttpOnly' in headers_str
    assert 'Set-Cookie: session=abc; Path=/' in headers_str
    # No other headers
    assert 'Content-Length' not in headers_str

def test_metadata_includes_elapsed_time_and_is_precise():
    resp = create_response()
    # Wait a bit to create measurable elapsed time
    time.sleep(0.02)
    http_resp = HTTPResponse(resp)
    meta = http_resp.metadata
    # Metadata should contain a single line with elapsed time
    assert meta.startswith('Elapsed Time: ')
    # Extract the numeric part
    elapsed_str = meta.split(': ')[1].rstrip('s')
    elapsed_val = float(elapsed_str)
    # The elapsed time should be at least the sum of elapsed and wait
    assert elapsed_val >= 0.02
    # Ensure the format has up to 10 decimal places
    assert len(elapsed_str.split('.')[1]) <= 10

def test_version_fallback_and_explicit_version():
    # Response with explicit HTTP/2.0 version
    resp = create_response()
    resp.raw = type('Raw', (), {'version': 20})()
    http_resp = HTTPResponse(resp)
    assert http_resp.version == '2.0'

    # Response without raw.version attribute should fallback to 1.1
    resp_no_raw = create_response()
    delattr(resp_no_raw, 'raw')
    http_resp_no_raw = HTTPResponse(resp_no_raw)
    assert http_resp_no_raw.version == '1.1'
