import re
import string
import pytest
from mimesis.providers.payment import Payment
from mimesis.enums import CardType, Gender

def test_credit_card_number_format_and_luhn():
    provider = Payment()
    # Visa card
    visa_number = provider.credit_card_number(CardType.VISA)
    assert re.fullmatch(r"\d{4} \d{4} \d{4} \d{4}", visa_number)
    # American Express card
    amex_number = provider.credit_card_number(CardType.AMERICAN_EXPRESS)
    assert re.fullmatch(r"\d{4} \d{6} \d{5}", amex_number)
    # Ensure Luhn checksum is correct for both
    def luhn_valid(number: str) -> bool:
        digits = [int(d) for d in number.replace(" ", "")]
        checksum = 0
        parity = len(digits) % 2
        for i, d in enumerate(digits):
            if i % 2 == parity:
                d *= 2
                if d > 9:
                    d -= 9
            checksum += d
        return checksum % 10 == 0
    assert luhn_valid(visa_number)
    assert luhn_valid(amex_number)

def test_credit_card_expiration_date_range():
    provider = Payment()
    # Test with default range
    exp_date = provider.credit_card_expiration_date()
    month, year = exp_date.split("/")
    assert 1 <= int(month) <= 12
    assert 16 <= int(year) <= 25
    # Test with custom range
    exp_date_custom = provider.credit_card_expiration_date(minimum=20, maximum=30)
    month_c, year_c = exp_date_custom.split("/")
    assert 1 <= int(month_c) <= 12
    assert 20 <= int(year_c) <= 30

def test_cvv_format_and_range():
    provider = Payment()
    cvv = provider.cvv()
    assert re.fullmatch(r"\d{3}", cvv)
    assert 1 <= int(cvv) <= 999
