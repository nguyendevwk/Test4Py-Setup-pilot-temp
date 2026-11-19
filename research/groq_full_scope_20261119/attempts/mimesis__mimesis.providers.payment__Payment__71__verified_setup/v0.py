import re
import string
import pytest
from mimesis.providers.payment import Payment
from mimesis.enums import CardType, Gender
from mimesis.exceptions import NonEnumerableError

def test_credit_card_number_and_cvv_format():
    provider = Payment()
    # Visa card number should start with 4 and be 16 digits formatted in groups of 4
    visa_number = provider.credit_card_number(CardType.VISA)
    assert re.fullmatch(r"\d{4} \d{4} \d{4} \d{4}", visa_number)
    assert visa_number.split()[0].startswith("4")
    # CVV should be a 3-digit string
    cvv = provider.cvv()
    assert re.fullmatch(r"\d{3}", cvv)

def test_bitcoin_address_and_cid_range():
    provider = Payment()
    # Bitcoin address must start with 1 or 3 and be 34 characters long
    btc_addr = provider.bitcoin_address()
    assert btc_addr[0] in ("1", "3")
    assert len(btc_addr) == 34
    assert re.fullmatch(r"[1-3][A-Za-z0-9]{33}", btc_addr)
    # CID should be a 4-digit string between 0001 and 9999
    cid = provider.cid()
    assert re.fullmatch(r"\d{4}", cid)
    assert 1 <= int(cid) <= 9999

def test_credit_card_number_invalid_type_raises():
    provider = Payment()
    # Passing an unsupported card type should raise NonEnumerableError
    with pytest.raises(NonEnumerableError):
        provider.credit_card_number(CardType(999))
