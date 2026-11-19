import re
import uuid as uuid_module
import pytest

from string_utils.generation import uuid


def test_uuid_default_representation():
    """The default uuid() should return a string with 5 groups separated by hyphens."""
    result = uuid()
    # UUID format: 8-4-4-4-12 hex digits
    pattern = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
    assert isinstance(result, str)
    assert pattern.match(result), f"Result does not match UUID format: {result}"
    # Ensure that calling again yields a different value
    second = uuid()
    assert result != second, "uuid() returned the same value twice"


def test_uuid_as_hex_representation():
    """When as_hex=True, uuid() should return a 32‑character hex string without hyphens."""
    result = uuid(as_hex=True)
    assert isinstance(result, str)
    assert len(result) == 32, f"Hex UUID length is not 32: {len(result)}"
    assert re.fullmatch(r"[0-9a-f]{32}", result), f"Result is not a valid hex string: {result}"
    # Ensure that calling again yields a different value
    second = uuid(as_hex=True)
    assert result != second, "uuid(as_hex=True) returned the same value twice"


def test_uuid_as_hex_with_non_bool_argument():
    """Passing a truthy non‑bool value should still return the hex representation."""
    result = uuid(as_hex=1)  # 1 is truthy
    assert isinstance(result, str)
    assert len(result) == 32
    assert re.fullmatch(r"[0-9a-f]{32}", result), f"Result is not a valid hex string: {result}"
