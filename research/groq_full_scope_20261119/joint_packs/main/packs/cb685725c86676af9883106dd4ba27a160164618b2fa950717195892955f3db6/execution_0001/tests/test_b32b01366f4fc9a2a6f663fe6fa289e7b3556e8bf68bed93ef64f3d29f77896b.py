import pytest
from pypara.monetary import IncompatibleCurrencyError

# Simple stand‑in for Currency with a `code` attribute
class DummyCurrency:
    def __init__(self, code: str):
        self.code = code

def test_incompatible_currency_error_message_and_attributes():
    ccy1 = DummyCurrency("USD")
    ccy2 = DummyCurrency("EUR")
    op = "addition"
    err = IncompatibleCurrencyError(ccy1, ccy2, op)
    # Check that the error message contains the expected parts
    assert str(err) == "USD vs EUR are incompatible for operation 'addition'."
    # Check that the attributes are stored correctly
    assert err.ccy1 is ccy1
    assert err.ccy2 is ccy2
    assert err.operation == op
    # Ensure it is a subclass of ValueError
    assert isinstance(err, ValueError)

def test_incompatible_currency_error_default_operation():
    ccy1 = DummyCurrency("GBP")
    ccy2 = DummyCurrency("JPY")
    err = IncompatibleCurrencyError(ccy1, ccy2)
    # Default operation should be "<Unspecified>"
    assert err.operation == "<Unspecified>"
    assert str(err) == "GBP vs JPY are incompatible for operation '<Unspecified>'."

def test_incompatible_currency_error_with_nonstandard_codes():
    ccy1 = DummyCurrency("X")
    ccy2 = DummyCurrency("Y")
    err = IncompatibleCurrencyError(ccy1, ccy2, "multiplication")
    # Even with single‑character codes, the message should format correctly
    assert str(err) == "X vs Y are incompatible for operation 'multiplication'."
    assert err.ccy1.code == "X"
    assert err.ccy2.code == "Y"
