import pytest
from string_utils.validation import is_credit_card

# Known valid card numbers for different types
VALID_CARDS = {
    "VISA": "4111111111111111",
    "MASTERCARD": "5500000000000004",
    "AMERICAN_EXPRESS": "378282246310005",
    "DINERS_CLUB": "30569309025904",
    "DISCOVER": "6011111111111117",
    "JCB": "3528000000000000",
}

def test_valid_cards_any_type():
    """
    Verify that a valid card number is accepted when no card_type is specified
    and that specifying a correct card_type also returns True.
    """
    # Any card type should be accepted
    for card_type, number in VALID_CARDS.items():
        assert is_credit_card(number) is True, f"{number} should be valid for any type"

    # Specific card type should also validate
    assert is_credit_card(VALID_CARDS["VISA"], "VISA") is True
    assert is_credit_card(VALID_CARDS["MASTERCARD"], "MASTERCARD") is True
    assert is_credit_card(VALID_CARDS["AMERICAN_EXPRESS"], "AMERICAN_EXPRESS") is True

def test_invalid_card_type_error():
    """
    Verify that providing an unsupported card_type raises a KeyError
    with an informative message.
    """
    with pytest.raises(KeyError) as excinfo:
        is_credit_card("4111111111111111", card_type="INVALID_TYPE")
    assert "Invalid card type" in str(excinfo.value)
    assert "VISA" in str(excinfo.value)  # ensure valid types are listed

def test_non_full_string_false():
    """
    Verify that strings containing non-digit characters or incomplete
    sequences are rejected, even if they match a known card pattern
    when dashes or spaces are removed.
    """
    # Commonly formatted Visa with dashes
    formatted_visa = "4111-1111-1111-1111"
    assert is_credit_card(formatted_visa) is False

    # Incomplete number (too short)
    short_number = "411111111111"
    assert is_credit_card(short_number) is False

    # Non-string input should also return False
    assert is_credit_card(1234567890123456) is False
