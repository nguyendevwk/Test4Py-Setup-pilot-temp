import time
import requests
from httpie.models import HTTPResponse

def test_headers_property_excludes_set_cookie_and_expands_cookies():
    # Prepare a fake response with a Set-Cookie header containing two cookies
    resp = requests.Response()
    resp.status_code = 200
    resp.reason = "OK"
    resp.url = "http://example.com"
    resp.headers = {
        "Content-Type": "text/plain",
        "Set-Cookie": "id=123; Path=/; HttpOnly, session=abc; Path=/",
    }
    resp._orig = resp  # mimic wrapper's internal reference
    # Wrap with HTTPResponse
    http_resp = HTTPResponse(resp)
    # The headers string should start with the status line
    assert http_resp.headers.startswith("HTTP/1.1 200 OK")
    # It should contain the Content-Type header
    assert "Content-Type: text/plain" in http_resp.headers
    # It should contain each cookie as a separate Set-Cookie line
    assert "Set-Cookie: id=123; Path=/; HttpOnly" in http_resp.headers
    assert "Set-Cookie: session=abc; Path=/" in http_resp.headers
    # It should not contain the original Set-Cookie header line
    assert "Set-Cookie: id=123; Path=/; HttpOnly, session=abc; Path=/" not in http_resp.headers

def test_metadata_includes_elapsed_time_and_is_precise():
    # Prepare a fake response with a known elapsed time
    resp = requests.Response()
    resp.status_code = 200
    resp.reason = "OK"
    resp.url = "http://example.com"
    resp.elapsed = time.timedelta(seconds=0.123456)
    # Simulate the time when headers were parsed
    resp._httpie_headers_parsed_at = time.monotonic() - 0.001234
    resp._orig = resp
    http_resp = HTTPResponse(resp)
    # The metadata should contain the elapsed time label
    assert "Elapsed time:" in http_resp.metadata
    # Extract the numeric part and verify it is close to the sum of elapsed and time since parsed
    elapsed_str = http_resp.metadata.splitlines()[0].split(":")[1].strip()
    elapsed_value = float(elapsed_str.rstrip("s"))
    expected = 0.123456 + 0.001234
    assert abs(elapsed_value - expected) < 1e-6

def test_version_mapping_returns_correct_http_version():
    # Prepare a fake response with raw version 11 (HTTP/1.1)
    resp = requests.Response()
    resp.status_code = 200
    resp.reason = "OK"
    resp.url = "http://example.com"
    # Mock the raw object with a version attribute
    class Raw:
        version = 11
    resp.raw = Raw()
    resp._orig = resp
    http_resp = HTTPResponse(resp)
    assert http_resp.version == "1.1"

    # Test fallback when raw has no version attribute
    resp.raw = object()
    http_resp = HTTPResponse(resp)
    assert http_resp.version == "1.1"

    # Test mapping for HTTP/2.0
    class Raw2:
        version = 20
    resp.raw = Raw2()
    http_resp = HTTPResponse(resp)
    assert http_resp.version == "2.0"
