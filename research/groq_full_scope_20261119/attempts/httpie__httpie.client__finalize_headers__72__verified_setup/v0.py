import pytest
from httpie.client import finalize_headers
from httpie.cli.dicts import HTTPHeadersDict
from urllib3.util import SKIPPABLE_HEADERS, SKIP_HEADER

def test_finalize_headers_encodes_and_strips():
    """Headers with leading/trailing whitespace and string values are stripped and encoded."""
    raw = HTTPHeadersDict()
    raw.add("X-Test-Header", "  value with spaces  ")
    raw.add("X-Another", "simple")
    raw.add("X-Number", 123)  # non-string, should stay unchanged

    final = finalize_headers(raw)

    # The header values should be stripped of whitespace
    assert final["X-Test-Header"] == b"value with spaces"
    assert final["X-Another"] == b"simple"
    # Non-string values should be unchanged
    assert final["X-Number"] == 123

def test_finalize_headers_skippable_headers():
    """Headers set to None that are skippable are replaced with SKIP_HEADER."""
    raw = HTTPHeadersDict()
    # Use a known skippable header
    skippable = next(iter(SKIPPABLE_HEADERS))
    raw.add(skippable, None)
    # Non-skippable header set to None should be omitted
    raw.add("Non-Skippable", None)

    final = finalize_headers(raw)

    # Skippable header should be present and set to SKIP_HEADER
    assert final[skippable] == SKIP_HEADER
    # Non-skippable header should not appear in the final headers
    assert "Non-Skippable" not in final

def test_finalize_headers_none_values_and_order():
    """Headers with None values that are not skippable are omitted, and order is preserved."""
    raw = HTTPHeadersDict()
    raw.add("Header-One", "value1")
    raw.add("Header-Two", None)          # non-skippable, should be omitted
    raw.add("Header-Three", "value3")

    final = finalize_headers(raw)

    # Only the non-None headers should be present
    assert list(final.keys()) == ["Header-One", "Header-Three"]
    assert final["Header-One"] == b"value1"
    assert final["Header-Three"] == b"value3"
