import pytest
from string_utils.validation import is_credit_card

def test_is_credit_card_valid_visa():
    # A known valid VISA number (16 digits, starts with 4)
    assert is_credit_card("4111111111111111") is True
    # Same number with spaces should be rejected because is_full_string requires exact match
    assert is_credit_card("4111 1111 1111 1111") is False

def test_is_credit_card_invalid_and_boundary():
    # Too short number
    assert is_credit_card("411111111111") is False
    # Non-digit characters
    assert is_credit_card("4111-1111-1111-1111") is False
    # Empty string
    assert is_credit_card("") is False
    # None input
    assert is_credit_card(None) is False

def test_is_credit_card_unknown_card_type_raises():
    with pytest.raises(KeyError) as excinfo:
        is_credit_card("4111111111111111", card_type="UNKNOWN")
    assert "Invalid card type" in str(excinfo.value)
