import pytest
from string_utils.validation import is_credit_card

# Known valid credit card numbers for each supported type
VALID_CARDS = {
    "VISA": "4111111111111111",
    "MASTERCARD": "5500000000000004",
    "AMERICAN_EXPRESS": "378282246310005",
    "DINERS_CLUB": "30569309025904",
    "DISCOVER": "6011111111111117",
    "JCB": "3528000000000000",
}

def test_is_credit_card_valid_any_type():
    """
    Verify that a valid card number is accepted when no card_type is specified.
    """
    # Pick a VISA number
    card = VALID_CARDS["VISA"]
    assert is_credit_card(card) is True

def test_is_credit_card_invalid_card_type_raises():
    """
    Verify that providing an unsupported card_type raises KeyError.
    """
    card = VALID_CARDS["VISA"]
    with pytest.raises(KeyError) as excinfo:
        is_credit_card(card, card_type="INVALID_TYPE")
    assert "Invalid card type" in str(excinfo.value)

def test_is_credit_card_boundary_empty_string():
    """
    Verify that an empty or whitespace-only string is rejected.
    """
    assert is_credit_card("") is False
    assert is_credit_card("   ") is False
