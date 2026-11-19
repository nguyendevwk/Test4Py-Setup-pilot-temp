import pytest
from string_utils.validation import is_credit_card

def test_valid_visa_card_returns_true():
    # A known valid VISA card number (16 digits, starts with 4)
    visa_number = "4111111111111111"
    assert is_credit_card(visa_number) is True
    assert is_credit_card(visa_number, card_type="VISA") is True

def test_invalid_card_type_raises_key_error():
    # Use a valid card number but request an unsupported card type
    card_number = "4111111111111111"
    with pytest.raises(KeyError) as excinfo:
        is_credit_card(card_number, card_type="INVALID_TYPE")
    assert "Invalid card type" in str(excinfo.value)
    assert "VISA" in str(excinfo.value)  # ensure valid types are listed

def test_non_string_input_returns_false():
    # Passing a non-string (e.g., integer) should return False, not raise
    assert is_credit_card(1234567890123456) is False
    assert is_credit_card(None) is False
    assert is_credit_card([1, 2, 3]) is False
