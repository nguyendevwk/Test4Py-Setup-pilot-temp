import pytest
from string_utils.validation import is_credit_card

# Test 1: Valid VISA card number (normal case)
def test_is_credit_card_valid_visa():
    # 16‑digit VISA number that passes Luhn check
    visa_number = "4111111111111111"
    assert is_credit_card(visa_number) is True
    assert is_credit_card(visa_number, card_type="VISA") is True
    # Should not match other card types
    assert is_credit_card(visa_number, card_type="MASTERCARD") is False

# Test 2: Boundary case – number with spaces and dashes (should be rejected)
def test_is_credit_card_with_separators():
    # VISA number with spaces and dashes
    formatted_number = "4111-1111 1111 1111"
    # The function expects a full string without separators
    assert is_credit_card(formatted_number) is False
    # Even when specifying card type, it should still reject
    assert is_credit_card(formatted_number, card_type="VISA") is False

# Test 3: Error case – invalid card type raises KeyError
def test_is_credit_card_invalid_card_type():
    with pytest.raises(KeyError) as excinfo:
        is_credit_card("4111111111111111", card_type="INVALID_TYPE")
    assert "Invalid card type" in str(excinfo.value)
    assert "VISA" in str(excinfo.value)  # ensure valid types are listed
