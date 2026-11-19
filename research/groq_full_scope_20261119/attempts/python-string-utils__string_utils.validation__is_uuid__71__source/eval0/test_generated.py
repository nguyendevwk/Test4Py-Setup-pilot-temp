import pytest
from string_utils.validation import is_uuid

def test_is_uuid_with_standard_form_and_invalid():
    # Valid standard UUID should return True
    assert is_uuid("6f8aa2f9-686c-4ac3-8766-5712354a04cf") is True
    # Invalid UUID missing hyphens should return False
    assert is_uuid("6f8aa2f9686c4ac387665712354a04cf") is False
    # Non-string input is cast to string; empty string is invalid
    assert is_uuid("") is False

def test_is_uuid_allow_hex_true():
    # Hex representation should be accepted when allow_hex=True
    hex_uuid = "6f8aa2f9686c4ac387665712354a04cf"
    assert is_uuid(hex_uuid, allow_hex=True) is True
    # Standard form should also be accepted with allow_hex=True
    assert is_uuid("6f8aa2f9-686c-4ac3-8766-5712354a04cf", allow_hex=True) is True

def test_is_uuid_invalid_inputs_and_edge_cases():
    # None is cast to string "None" which is not a UUID
    assert is_uuid(None) is False
    # Integer input is cast to string and should be invalid
    assert is_uuid(12345) is False
    # UUID with wrong length but correct hyphen pattern should be invalid
    assert is_uuid("12345678-1234-1234-1234-1234567890ab") is False
