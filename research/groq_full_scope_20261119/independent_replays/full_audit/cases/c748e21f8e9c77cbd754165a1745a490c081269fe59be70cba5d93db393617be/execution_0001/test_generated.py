import re
import uuid as uuid_module
import pytest

from string_utils.generation import uuid


def test_uuid_default_format(tmp_path):
    """uuid() should return a 36‑character string with hyphens in the correct positions."""
    result = uuid()
    # UUID format: 8-4-4-4-12 hex digits
    assert isinstance(result, str)
    assert len(result) == 36
    pattern = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
    assert pattern.match(result)
    # Ensure it can be parsed back to a UUID object
    parsed = uuid_module.UUID(result)
    assert str(parsed) == result


def test_uuid_hex_format(tmp_path):
    """uuid(as_hex=True) should return a 32‑character hex string without hyphens."""
    result = uuid(as_hex=True)
    assert isinstance(result, str)
    assert len(result) == 32
    assert re.fullmatch(r"[0-9a-f]{32}", result)
    # Ensure it can be parsed back to a UUID object
    parsed = uuid_module.UUID(result)
    assert parsed.hex == result


def test_uuid_non_bool_as_hex(tmp_path):
    """Passing a non‑boolean to as_hex should still be interpreted as a truthy/falsy value."""
    # Truthy non‑bool: string "yes"
    result_truthy = uuid(as_hex="yes")
    assert isinstance(result_truthy, str)
    assert len(result_truthy) == 32
    # Falsy non‑bool: empty string
    result_falsy = uuid(as_hex="")
    assert isinstance(result_falsy, str)
    assert len(result_falsy) == 36
    # Ensure both can be parsed back
    assert uuid_module.UUID(result_truthy).hex == result_truthy
    assert uuid_module.UUID(result_falsy).hex == result_falsy.replace("-", "")
