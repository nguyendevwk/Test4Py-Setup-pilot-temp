import pytest
from httpie.cli.dicts import HTTPHeadersDict
from httpie.client import finalize_headers
from urllib3.util import SKIP_HEADER, SKIPPABLE_HEADERS

def test_finalize_headers_encodes_and_strips_strings():
    # Header value with leading/trailing whitespace should be stripped and encoded
    headers = HTTPHeadersDict({"X-Custom": "  value  "})
    final = finalize_headers(headers)
    # The value should be bytes, not str, and whitespace removed
    assert isinstance(final["X-Custom"], bytes)
    assert final["X-Custom"] == b"value"

def test_finalize_headers_skips_none_for_skippable_headers():
    # Headers that are skippable should be replaced with SKIP_HEADER when set to None
    for name in SKIPPABLE_HEADERS:
        headers = HTTPHeadersDict({name: None})
        final = finalize_headers(headers)
        assert final[name] == SKIP_HEADER

def test_finalize_headers_ignores_none_for_non_skippable_headers():
    # Non-skippable headers set to None should be omitted from the result
    headers = HTTPHeadersDict({"Non-Skippable": None})
    final = finalize_headers(headers)
    assert "Non-Skippable" not in final
