import pytest
from pypara.monetary import IncompatibleCurrencyError
from pypara.currencies import Currency

def test_incompatible_currency_error_default_operation():
    """Test that the default operation string is used when none is provided."""
    ccy1 = Currency("USD")
    ccy2 = Currency("EUR")
    error = IncompatibleCurrencyError(ccy1, ccy2)
    assert error.ccy1 is ccy1
    assert error.ccy2 is ccy2
    assert error.operation == "<Unspecified>"
    expected_msg = f"{ccy1.code} vs {ccy2.code} are incompatible for operation '<Unspecified>'."
    assert str(error) == expected_msg

def test_incompatible_currency_error_custom_operation():
    """Test that a custom operation string is reflected in the error."""
    ccy1 = Currency("JPY")
    ccy2 = Currency("GBP")
    operation = "addition"
    error = IncompatibleCurrencyError(ccy1, ccy2, operation)
    assert error.operation == operation
    expected_msg = f"{ccy1.code} vs {ccy2.code} are incompatible for operation '{operation}'."
    assert str(error) == expected_msg

def test_incompatible_currency_error_message_contains_codes():
    """Ensure the error message includes both currency codes."""
    ccy1 = Currency("CHF")
    ccy2 = Currency("AUD")
    error = IncompatibleCurrencyError(ccy1, ccy2, "subtraction")
    msg = str(error)
    assert ccy1.code in msg
    assert ccy2.code in msg
    assert "subtraction" in msg
