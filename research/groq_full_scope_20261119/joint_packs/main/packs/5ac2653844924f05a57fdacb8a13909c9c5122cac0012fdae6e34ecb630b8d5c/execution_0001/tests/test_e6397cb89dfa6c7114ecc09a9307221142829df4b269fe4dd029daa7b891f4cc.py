import re
import string

import pytest

from string_utils.generation import uuid


def test_uuid_default_format():
    """uuid() should return a standard UUID string with hyphens."""
    result = uuid()
    # UUID pattern: 8-4-4-4-12 hex digits
    pattern = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
    assert isinstance(result, str), "Result should be a string"
    assert pattern.match(result), f"Result '{result}' does not match UUID format"


def test_uuid_hex_format():
    """uuid(as_hex=True) should return a 32‑character hexadecimal string."""
    result = uuid(as_hex=True)
    assert isinstance(result, str), "Result should be a string"
    assert len(result) == 32, f"Hex string length should be 32, got {len(result)}"
    assert all(c in string.hexdigits.lower() for c in result), (
        "Hex string contains non‑hexadecimal characters"
    )


def test_uuid_uniqueness():
    """Multiple calls to uuid() should produce distinct values."""
    first = uuid()
    second = uuid()
    assert first != second, "Two consecutive UUIDs should not be equal"
