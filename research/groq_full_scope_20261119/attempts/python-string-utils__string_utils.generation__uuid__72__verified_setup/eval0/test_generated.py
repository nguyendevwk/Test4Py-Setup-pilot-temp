import re
import uuid as py_uuid
import string
import random
import pytest

from string_utils.generation import uuid


def test_uuid_default_format():
    """The default uuid() should return a string in the canonical 8-4-4-4-12 format."""
    result = uuid()
    # Pattern: 8 hex, dash, 4 hex, dash, 4 hex, dash, 4 hex, dash, 12 hex
    pattern = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
    assert pattern.match(result), f"Result '{result}' does not match UUID format"
    # Ensure the string is not the same as a freshly generated uuid4 from stdlib
    assert result != str(py_uuid.uuid4()), "uuid() returned a duplicate of a freshly generated UUID"


def test_uuid_as_hex_returns_32_hex_digits():
    """When as_hex=True, uuid() should return a 32‑character hexadecimal string."""
    result = uuid(as_hex=True)
    assert isinstance(result, str), "Result is not a string"
    assert len(result) == 32, f"Hex string length is {len(result)}, expected 32"
    assert all(c in string.hexdigits.lower() for c in result), "Hex string contains non‑hex characters"


def test_uuid_uniqueness_over_multiple_calls():
    """Multiple calls to uuid() should produce distinct values."""
    results = {uuid() for _ in range(10)}
    # 10 UUIDs should all be unique
    assert len(results) == 10, "Duplicate UUIDs generated"
    # Ensure each UUID matches the canonical format
    pattern = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
    for r in results:
        assert pattern.match(r), f"UUID '{r}' does not match expected format"
