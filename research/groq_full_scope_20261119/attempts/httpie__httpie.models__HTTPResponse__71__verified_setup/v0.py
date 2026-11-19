import time
import requests
from httpie.models import HTTPResponse
from urllib3.util import SKIP_HEADER, SKIPPABLE_HEADERS
from httpie.utils import split_cookies

def create_response(status=200, headers=None, body=b''):
    """Helper to create a minimal requests.Response."""
    resp = requests.Response()
    resp.status_code = status
    resp._content = body
    resp.headers = headers or {}
    # set elapsed to a small timedelta
    resp.elapsed = time.timedelta(seconds=0.001)
    # fake raw attributes for version detection
    class Raw:
        version = 11
    resp.raw = Raw()
    # fake httpie header parsed time
    resp._httpie_headers_parsed_at = time.monotonic()
    return resp

def test_headers_property_excludes_set_cookie_and_splits_cookies():
    resp = create_response(
        status=200,
        headers={
            'Content-Type': 'text/plain',
            'Set-Cookie': 'id=123; Path=/; HttpOnly, token=abc; Path=/'
        }
    )
    http_resp = HTTPResponse(resp)
    headers_str = http_resp.headers
    # status line present
    assert headers_str.startswith('HTTP/1.1 200 OK')
    # Content-Type header present
    assert 'Content-Type: text/plain' in headers_str
    # Set-Cookie headers split into separate lines
    assert headers_str.count('Set-Cookie:') == 2
    assert 'Set-Cookie: id=123; Path=/; HttpOnly' in headers_str
    assert 'Set-Cookie: token=abc; Path=/' in headers_str
    # No duplicate Set-Cookie header line
    assert headers_str.count('Set-Cookie: id=123; Path=/; HttpOnly, token=abc; Path=/') == 0

def test_metadata_includes_elapsed_time_and_is_numeric():
    resp = create_response()
    http_resp = HTTPResponse(resp)
    meta = http_resp.metadata
    # metadata should contain a single line with elapsed time
    assert meta.startswith('Elapsed time: ')
    # extract numeric part
    elapsed_str = meta.split(': ')[1].rstrip('s')
    elapsed_val = float(elapsed_str)
    # elapsed time should be at least the elapsed attribute (0.001s)
    assert elapsed_val >= 0.001

def test_version_fallback_and_custom_raw_version():
    # Response with custom raw version 20 (HTTP/2.0)
    class RawV20:
        version = 20
    resp = create_response()
    resp.raw = RawV20()
    http_resp = HTTPResponse(resp)
    assert http_resp.version == '2.0'

    # Response with no raw.version attribute triggers fallback to 1.1
    class RawNoVer:
        pass
    resp.raw = RawNoVer()
    http_resp = HTTPResponse(resp)
    assert http_resp.version == '1.1'
