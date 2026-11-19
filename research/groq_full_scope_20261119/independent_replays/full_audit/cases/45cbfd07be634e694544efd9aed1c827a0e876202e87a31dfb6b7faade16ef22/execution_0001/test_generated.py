import re
import string
import pytest
from mimesis.providers.payment import Payment
from mimesis.enums import CardType, Gender
from mimesis.exceptions import NonEnumerableError


def test_credit_card_number_visa_format_and_luhn():
    """Verify that a Visa card number is 16 digits, correctly grouped, and passes Luhn."""
    payment = Payment(seed=123)
    number = payment.credit_card_number(CardType.VISA)
    # Remove spaces and check length
    digits = number.replace(" ", "")
    assert len(digits) == 16
    assert digits.isdigit()
    # Check grouping pattern
    assert re.fullmatch(r"\d{4} \d{4} \d{4} \d{4}", number)
    # Verify Luhn checksum
    def luhn_valid(num: str) -> bool:
        total = 0
        reverse_digits = num[::-1]
        for i, d in enumerate(reverse_digits):
            n = int(d)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        return total % 10 == 0
    assert luhn_valid(digits)


def test_credit_card_number_unsupported_type_raises():
    """Ensure that passing an unsupported CardType raises NonEnumerableError."""
    payment = Payment(seed=123)
    class DummyCardType:
        pass
    with pytest.raises(NonEnumerableError):
        payment.credit_card_number(DummyCardType)  # type: ignore[arg-type]


def test_bitcoin_address_format_and_length():
    """Check that a bitcoin address starts with 1 or 3 and has correct length."""
    payment = Payment(seed=123)
    address = payment.bitcoin_address()
    assert address[0] in ("1", "3")
    assert len(address) == 34
    # Ensure all characters are alphanumeric
    assert all(c in string.ascii_letters + string.digits for c in address[1:])
