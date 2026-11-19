import pytest
from pypara.monetary import IncompatibleCurrencyError

# Simple stand‑in for the real Currency type used in the library.
class DummyCurrency:
    def __init__(self, code: str):
        self.code = code

def test_incompatible_currency_error_message_and_attributes():
    """The error should store the currencies and operation and format the message correctly."""
    ccy1 = DummyCurrency("USD")
    ccy2 = DummyCurrency("EUR")
    op = "addition"
    err = IncompatibleCurrencyError(ccy1, ccy2, op)

    # The message should contain both currency codes and the operation name.
    assert str(err) == "USD vs EUR are incompatible for operation 'addition'."

    # The attributes should be accessible and match the inputs.
    assert err.ccy1 is ccy1
    assert err.ccy2 is ccy2
    assert err.operation == op

def test_incompatible_currency_error_default_operation():
    """When no operation is supplied, the default placeholder should appear in the message."""
    ccy1 = DummyCurrency("JPY")
    ccy2 = DummyCurrency("GBP")
    err = IncompatibleCurrencyError(ccy1, ccy2)

    # Default operation placeholder is used.
    assert str(err) == "JPY vs GBP are incompatible for operation '<Unspecified>'."

    # The operation attribute should be the default string.
    assert err.operation == "<Unspecified>"

def test_incompatible_currency_error_is_value_error_subclass():
    """The custom error must inherit from ValueError and behave accordingly."""
    ccy1 = DummyCurrency("AUD")
    ccy2 = DummyCurrency("CAD")
    err = IncompatibleCurrencyError(ccy1, ccy2, "subtraction")

    # It should be an instance of ValueError.
    assert isinstance(err, ValueError)

    # Raising the error should be caught by a ValueError handler.
    with pytest.raises(ValueError) as excinfo:
        raise err
    assert excinfo.value is err
