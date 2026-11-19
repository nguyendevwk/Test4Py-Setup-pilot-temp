import pytest
from httpie.client import finalize_headers
from httpie.cli.dicts import HTTPHeadersDict
from urllib3.util import SKIPPABLE_HEADERS, SKIP_HEADER

def test_finalize_headers_encodes_and_strips():
    """Headers with leading/trailing whitespace and string values are stripped and encoded."""
    raw = HTTPHeadersDict()
    raw.add("X-Test-Header", "  value with spaces  ")
    raw.add("X-Another", "simple")
    raw.add("X-Empty", None)

    final = finalize_headers(raw)

    # The header values should be stripped of whitespace and encoded to bytes
    assert final["X-Test-Header"] == b"value with spaces"
    assert final["X-Another"] == b"simple"
    # None values should be omitted
    assert "X-Empty" not in final

def test_finalize_headers_skippable_headers():
    """Headers that are skippable and set to None are replaced with SKIP_HEADER."""
    raw = HTTPHeadersDict()
    # Pick a known skippable header
    skippable = next(iter(SKIPPABLE_HEADERS))
    raw.add(skippable, None)

    final = finalize_headers(raw)

    # The skippable header should be present and set to SKIP_HEADER
    assert final[skippable] == SKIP_HEADER

def test_finalize_headers_mixed_types_and_order():
    """Headers with mixed types preserve order and correctly handle non-string values."""
    raw = HTTPHeadersDict()
    raw.add("X-Int", 123)          # non-string, should stay as is
    raw.add("X-None", None)        # None, should be omitted
    raw.add("X-Bytes", b"bytes")   # bytes, should stay as is

    final = finalize_headers(raw)

    # Order preserved: X-Int first, then X-Bytes
    keys = list(final.keys())
    assert keys == ["X-Int", "X-Bytes"]

    # Values unchanged for non-string types
    assert final["X-Int"] == 123
    assert final["X-Bytes"] == b"bytes"

    # X-None omitted
    assert "X-None" not in final
