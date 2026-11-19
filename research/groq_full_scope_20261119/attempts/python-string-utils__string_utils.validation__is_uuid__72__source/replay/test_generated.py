import pytest
from string_utils.validation import is_uuid

def test_is_uuid_valid_standard_format():
    """A correctly formatted UUID should return True."""
    uuid_str = "6f8aa2f9-686c-4ac3-8766-5712354a04cf"
    assert is_uuid(uuid_str) is True

def test_is_uuid_invalid_and_hex_allowed():
    """A hex-only string should return False unless allow_hex is True."""
    hex_str = "6f8aa2f9686c4ac387665712354a04cf"
    assert is_uuid(hex_str) is False
    assert is_uuid(hex_str, allow_hex=True) is True

def test_is_uuid_non_string_input_and_boundary():
    """Non-string inputs are cast to string; empty string is invalid."""
    assert is_uuid(12345) is False
    assert is_uuid("") is False
