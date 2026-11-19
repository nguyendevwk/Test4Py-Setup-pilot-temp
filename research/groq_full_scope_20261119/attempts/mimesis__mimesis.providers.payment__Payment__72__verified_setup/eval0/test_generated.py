import re
import string
import pytest
from mimesis.providers.payment import Payment
from mimesis.enums import CardType, Gender

# Test 1: Verify that a Visa credit card number is 16 digits, starts with 4, and passes Luhn checksum
def test_credit_card_number_visa_valid():
    provider = Payment(seed=123)
    number = provider.credit_card_number(CardType.VISA)
    # Remove spaces
    digits = number.replace(" ", "")
    assert len(digits) == 16
    assert digits[0] == "4"
    # Luhn checksum: last digit should be correct
    def luhn_checksum(num: str) -> str:
        def digits_of(n):
            return [int(d) for d in n]
        digits = digits_of(num)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(str(d * 2)))
        return str((10 - (checksum % 10)) % 10)
    assert digits[-1] == luhn_checksum(digits[:-1])

# Test 2: Verify that requesting an unsupported card type raises NonEnumerableError
def test_credit_card_number_unsupported_type():
    provider = Payment(seed=456)
    with pytest.raises(Exception) as excinfo:
        provider.credit_card_number(CardType("NON_EXISTENT"))
    assert "NonEnumerableError" in str(excinfo.value)

# Test 3: Verify that a bitcoin address starts with 1 or 3 and has correct length
def test_bitcoin_address_format():
    provider = Payment(seed=789)
    address = provider.bitcoin_address()
    assert address[0] in ("1", "3")
    assert len(address) == 34
    # Ensure all characters are alphanumeric
    assert re.fullmatch(r"[13][A-Za-z0-9]{33}", address)
