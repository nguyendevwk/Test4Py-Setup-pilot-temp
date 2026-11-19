import pytest
from string_utils.validation import is_uuid

def test_is_uuid_valid_standard_format():
    # A correctly formatted UUID should return True
    uuid_str = "6f8aa2f9-686c-4ac3-8766-5712354a04cf"
    assert is_uuid(uuid_str) is True

def test_is_uuid_invalid_and_hex_behavior():
    # A UUID without hyphens is invalid unless allow_hex=True
    hex_uuid = "6f8aa2f9686c4ac387665712354a04cf"
    assert is_uuid(hex_uuid) is False
    assert is_uuid(hex_uuid, allow_hex=True) is True

def test_is_uuid_non_string_input_and_edge_cases():
    # Non-string inputs are cast to string; invalid formats return False
    assert is_uuid(12345) is False
    assert is_uuid(None) is False
    # Empty string is not a valid UUID
    assert is_uuid("") is False
