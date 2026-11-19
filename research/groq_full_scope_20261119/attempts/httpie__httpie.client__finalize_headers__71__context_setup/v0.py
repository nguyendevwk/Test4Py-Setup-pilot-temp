import pytest
from httpie.cli.dicts import HTTPHeadersDict
from httpie.client import finalize_headers
from urllib3.util import SKIP_HEADER, SKIPPABLE_HEADERS

def test_finalize_headers_encodes_and_strips_string_values():
    # Header with leading/trailing whitespace and a normal string value
    headers = HTTPHeadersDict({"X-Custom": "  value  ", "Accept": "application/json"})
    final = finalize_headers(headers)
    # The values should be stripped and encoded to bytes
    assert final["X-Custom"] == b"value"
    assert final["Accept"] == b"application/json"
    # The original dict should remain unchanged
    assert headers["X-Custom"] == "  value  "

def test_finalize_headers_skips_none_for_skippable_headers():
    # Header that is skippable and set to None
    headers = HTTPHeadersDict({"Connection": None, "User-Agent": "test"})
    final = finalize_headers(headers)
    # Skippable header should be replaced with SKIP_HEADER
    assert final["Connection"] == SKIP_HEADER
    # Non-skippable header should be preserved
    assert final["User-Agent"] == b"test"

def test_finalize_headers_removes_non_skippable_none_headers():
    # Header that is not skippable and set to None
    headers = HTTPHeadersDict({"X-Empty": None, "Content-Type": "text/plain"})
    final = finalize_headers(headers)
    # Non-skippable None header should be omitted entirely
    assert "X-Empty" not in final
    # The other header should be encoded
    assert final["Content-Type"] == b"text/plain"
