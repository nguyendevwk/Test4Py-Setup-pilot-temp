import re
import uuid

from string_utils.generation import uuid as uuid_func


def test_uuid_default_format():
    """UUID returned in default string format contains hyphens and matches the RFC 4122 pattern."""
    result = uuid_func()
    # Pattern for a standard UUID: 8-4-4-4-12 hex digits
    pattern = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
    assert isinstance(result, str), "Result should be a string"
    assert pattern.match(result), f"Result '{result}' does not match UUID pattern"


def test_uuid_hex_format():
    """UUID returned with as_hex=True has no hyphens and is 32 hex characters."""
    result = uuid_func(as_hex=True)
    assert isinstance(result, str), "Result should be a string"
    assert len(result) == 32, f"Hex UUID should be 32 characters, got {len(result)}"
    assert re.fullmatch(r"[0-9a-f]{32}", result), f"Result '{result}' is not a valid hex UUID"


def test_uuid_uniqueness():
    """Two consecutive calls to uuid() should produce distinct values."""
    first = uuid_func()
    second = uuid_func()
    assert first != second, "Consecutive UUIDs should be unique"
