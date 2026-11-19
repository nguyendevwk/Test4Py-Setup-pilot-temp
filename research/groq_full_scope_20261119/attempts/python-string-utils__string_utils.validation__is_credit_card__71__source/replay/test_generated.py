import pytest
from string_utils.validation import is_credit_card

def test_is_credit_card_valid_and_invalid_numbers():
    # Valid VISA card number (16 digits, starts with 4)
    assert is_credit_card("4111111111111111") is True
    # Invalid number: wrong length
    assert is_credit_card("411111111111") is False
    # Invalid number: contains non-digit characters
    assert is_credit_card("4111-1111-1111-1111") is False

def test_is_credit_card_with_specific_type_and_error():
    # Valid MasterCard number (16 digits, starts with 51-55)
    assert is_credit_card("5500000000000004", card_type="MASTERCARD") is True
    # Invalid for specified type: VISA number but asked for MasterCard
    assert is_credit_card("4111111111111111", card_type="MASTERCARD") is False
    # Unsupported card type should raise KeyError
    with pytest.raises(KeyError):
        is_credit_card("4111111111111111", card_type="UNKNOWN_CARD")

def test_is_credit_card_boundary_cases():
    # Boundary: minimum length for American Express (15 digits)
    assert is_credit_card("378282246310005", card_type="AMERICAN_EXPRESS") is True
    # Boundary: maximum length for Discover (16 digits)
    assert is_credit_card("6011111111111117", card_type="DISCOVER") is True
    # Edge: empty string should be invalid
    assert is_credit_card("") is False
