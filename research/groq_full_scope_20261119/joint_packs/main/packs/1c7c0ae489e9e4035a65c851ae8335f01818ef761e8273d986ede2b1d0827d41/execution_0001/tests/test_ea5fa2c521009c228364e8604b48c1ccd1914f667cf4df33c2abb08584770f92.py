import re
import uuid as uuid_module
import pytest
from string_utils.generation import uuid

# Regular expression for the standard UUID format
UUID_REGEX = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
)

# Regular expression for the 32‑character hexadecimal representation
HEX_REGEX = re.compile(r"^[0-9a-f]{32}$")


def test_uuid_default_format():
    """The default uuid() call should return a string matching the canonical UUID format."""
    result = uuid()
    assert isinstance(result, str), "uuid() should return a string"
    assert UUID_REGEX.match(result), f"Result '{result}' does not match UUID format"


def test_uuid_as_hex_format():
    """When as_hex=True, uuid() should return a 32‑character hexadecimal string."""
    result = uuid(as_hex=True)
    assert isinstance(result, str), "uuid(as_hex=True) should return a string"
    assert HEX_REGEX.match(result), f"Result '{result}' does not match 32‑hex format"
    # Ensure that the hex string is the concatenation of the parts of the canonical form
    canonical = str(uuid_module.UUID(result))
    assert canonical.replace("-", "") == result, "Hex string does not correspond to canonical UUID"


def test_uuid_uniqueness():
    """Multiple calls to uuid() should produce distinct values."""
    first = uuid()
    second = uuid()
    assert first != second, "Consecutive uuid() calls returned the same value"
    # Also test uniqueness for the hex variant
    first_hex = uuid(as_hex=True)
    second_hex = uuid(as_hex=True)
    assert first_hex != second_hex, "Consecutive uuid(as_hex=True) calls returned the same value"
