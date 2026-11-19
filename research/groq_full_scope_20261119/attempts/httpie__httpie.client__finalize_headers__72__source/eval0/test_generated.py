import pytest
from httpie.client import finalize_headers
from httpie.cli.dicts import HTTPHeadersDict
from urllib3.util import SKIPPABLE_HEADERS, SKIP_HEADER

def test_finalize_headers_encodes_and_strips():
    """Headers with leading/trailing whitespace and string values are stripped and encoded."""
    raw = HTTPHeadersDict()
    raw.add("X-Test-Header", "  value with spaces  ")
    raw.add("X-Empty", "   ")
    raw.add("X-Number", 123)  # non-string, should stay unchanged

    final = finalize_headers(raw)

    # The header value should be stripped and encoded to bytes
    assert final["X-Test-Header"] == b"value with spaces"
    # Empty string becomes b"" after stripping
    assert final["X-Empty"] == b""
    # Non-string values are left untouched
    assert final["X-Number"] == 123

def test_finalize_headers_skippable_headers_with_none():
    """Headers set to None that are skippable should be replaced with SKIP_HEADER."""
    raw = HTTPHeadersDict()
    for name in SKIPPABLE_HEADERS:
        raw.add(name, None)

    final = finalize_headers(raw)

    for name in SKIPPABLE_HEADERS:
        assert final[name] == SKIP_HEADER

def test_finalize_headers_non_skippable_none_ignored():
    """Headers set to None that are not skippable are omitted from the result."""
    raw = HTTPHeadersDict()
    raw.add("X-Non-Skippable", None)
    raw.add("Content-Type", "text/plain")

    final = finalize_headers(raw)

    # Non-skippable None header should not appear
    assert "X-Non-Skippable" not in final
    # Content-Type should be preserved and encoded
    assert final["Content-Type"] == b"text/plain"
