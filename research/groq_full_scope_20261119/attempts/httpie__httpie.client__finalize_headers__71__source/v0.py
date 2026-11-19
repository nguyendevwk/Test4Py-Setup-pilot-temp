import pytest
from httpie.client import finalize_headers
from httpie.cli.dicts import HTTPHeadersDict
from urllib3.util import SKIP_HEADER, SKIPPABLE_HEADERS

def test_finalize_headers_stripping_and_encoding():
    # Header value with leading/trailing whitespace and a string type
    headers = HTTPHeadersDict({"X-Custom": "  value  "})
    final = finalize_headers(headers)
    # Value should be stripped and encoded to bytes
    assert final["X-Custom"] == b"value"

def test_finalize_headers_skippable_header_none():
    # Header that is skippable and set to None should be replaced with SKIP_HEADER
    headers = HTTPHeadersDict({"Connection": None})
    final = finalize_headers(headers)
    assert final["Connection"] == SKIP_HEADER
    # Non-skippable header with None should be omitted
    headers = HTTPHeadersDict({"X-Ignore": None})
    final = finalize_headers(headers)
    assert "X-Ignore" not in final

def test_finalize_headers_multiple_headers_and_order():
    # Mixed headers: some normal, some skippable, some None
    headers = HTTPHeadersDict({
        "Accept": " application/json ",
        "Keep-Alive": None,
        "X-Token": " token ",
        "Transfer-Encoding": None
    })
    final = finalize_headers(headers)
    # Normal headers are stripped and encoded
    assert final["Accept"] == b"application/json"
    assert final["X-Token"] == b"token"
    # Skippable headers are replaced with SKIP_HEADER
    assert final["Keep-Alive"] == SKIP_HEADER
    assert final["Transfer-Encoding"] == SKIP_HEADER
    # Ensure no unexpected headers
    assert set(final.keys()) == {"Accept", "Keep-Alive", "X-Token", "Transfer-Encoding"}
