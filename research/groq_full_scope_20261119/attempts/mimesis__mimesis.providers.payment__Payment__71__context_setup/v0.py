import re
import string
import pytest
from mimesis.providers.payment import Payment
from mimesis.enums import CardType, Gender
from mimesis.exceptions import NonEnumerableError

# ---------------------------------------------------------------------------

def test_credit_card_number_and_luhn():
    """Test that credit card numbers are correctly formatted and pass Luhn check."""
    provider = Payment()
    # Visa card
    visa_num = provider.credit_card_number(CardType.VISA)
    assert re.fullmatch(r"\d{4} \d{4} \d{4} \d{4}", visa_num)
    # MasterCard card
    mc_num = provider.credit_card_number(CardType.MASTER_CARD)
    assert re.fullmatch(r"\d{4} \d{4} \d{4} \d{4}", mc_num)
    # American Express card
    amex_num = provider.credit_card_number(CardType.AMERICAN_EXPRESS)
    assert re.fullmatch(r"\d{4} \d{6} \d{5}", amex_num)

    # Helper to verify Luhn checksum
    def luhn_valid(number: str) -> bool:
        digits = [int(d) for d in number if d.isdigit()]
        checksum = 0
        parity = len(digits) % 2
        for i, d in enumerate(digits):
            if i % 2 == parity:
                d *= 2
                if d > 9:
                    d -= 9
            checksum += d
        return checksum % 10 == 0

    assert luhn_valid(visa_num.replace(" ", ""))
    assert luhn_valid(mc_num.replace(" ", ""))
    assert luhn_valid(amex_num.replace(" ", ""))

# ---------------------------------------------------------------------------

def test_bitcoin_address_format_and_length():
    """Test that bitcoin addresses start with 1 or 3 and have correct length."""
    provider = Payment()
    addr = provider.bitcoin_address()
    assert addr[0] in ("1", "3")
    assert len(addr) == 34
    # Ensure only alphanumeric characters after the first digit
    assert re.fullmatch(r"[13][A-Za-z0-9]{33}", addr)

# ---------------------------------------------------------------------------

def test_credit_card_number_unsupported_type_raises():
    """Test that providing an unsupported card type raises NonEnumerableError."""
    provider = Payment()
    with pytest.raises(NonEnumerableError):
        provider.credit_card_number(CardType(999))  # invalid enum value
