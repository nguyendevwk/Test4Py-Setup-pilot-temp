import re
import string
import pytest
from mimesis.providers.payment import Payment
from mimesis.enums import CardType, Gender

def test_credit_card_number_format_and_luhn():
    p = Payment()
    # Test Visa card number format and Luhn checksum
    visa_number = p.credit_card_number(CardType.VISA)
    assert re.fullmatch(r"\d{4} \d{4} \d{4} \d{4}", visa_number)
    digits = visa_number.replace(" ", "")
    assert len(digits) == 16
    # Luhn checksum: last digit should be correct
    assert digits[-1] == str(p.luhn_checksum(digits[:-1]))

    # Test American Express card number format and length
    amex_number = p.credit_card_number(CardType.AMERICAN_EXPRESS)
    assert re.fullmatch(r"\d{4} \d{6} \d{5}", amex_number)
    digits = amex_number.replace(" ", "")
    assert len(digits) == 15
    assert digits[-1] == str(p.luhn_checksum(digits[:-1]))

def test_credit_card_expiration_date_range():
    p = Payment()
    # Generate multiple dates to cover range
    for _ in range(10):
        exp_date = p.credit_card_expiration_date(minimum=20, maximum=30)
        month, year = exp_date.split("/")
        assert month.isdigit() and 1 <= int(month) <= 12
        assert year.isdigit() and 20 <= int(year) <= 30

def test_cvv_randomness_and_format():
    p = Payment()
    cvvs = {p.cvv() for _ in range(20)}
    # Ensure uniqueness in a small sample
    assert len(cvvs) > 1
    for cvv in cvvs:
        assert re.fullmatch(r"\d{3}", cvv)
        assert 1 <= int(cvv) <= 999
