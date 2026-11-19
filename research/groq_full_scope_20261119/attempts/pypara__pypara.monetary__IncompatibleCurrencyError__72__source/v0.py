import pytest
from pypara.monetary import IncompatibleCurrencyError

# Simple stand‑in for the Currency type used in the error
class DummyCurrency:
    def __init__(self, code: str):
        self.code = code

def test_incompatible_currency_error_message_and_attributes():
    """The error should expose the two currencies and the operation in its message."""
    ccy1 = DummyCurrency("USD")
    ccy2 = DummyCurrency("EUR")
    err = IncompatibleCurrencyError(ccy1, ccy2, operation="addition")
    # The message should contain both currency codes and the operation name
    assert "USD" in str(err)
    assert "EUR" in str(err)
    assert "addition" in str(err)
    # The attributes should be set correctly
    assert err.ccy1 is ccy1
    assert err.ccy2 is ccy2
    assert err.operation == "addition"

def test_incompatible_currency_error_default_operation():
    """When no operation is supplied, the default placeholder should appear."""
    ccy1 = DummyCurrency("JPY")
    ccy2 = DummyCurrency("GBP")
    err = IncompatibleCurrencyError(ccy1, ccy2)
    # Default operation placeholder is "<Unspecified>"
    assert "<Unspecified>" in str(err)
    assert err.operation == "<Unspecified>"

def test_incompatible_currency_error_is_value_error_subclass():
    """The custom error must inherit from ValueError."""
    ccy1 = DummyCurrency("AUD")
    ccy2 = DummyCurrency("CAD")
    err = IncompatibleCurrencyError(ccy1, ccy2, operation="subtraction")
    # isinstance should confirm subclass relationship
    assert isinstance(err, ValueError)
    # The error should not be caught by a generic Exception handler that expects a different type
    with pytest.raises(ValueError) as excinfo:
        raise err
    assert excinfo.value is err
