import pytest
from datetime import date
from pypara.exchange import FXRateLookupError
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date

# Helper to create a dummy Currency instance (assuming Currency accepts a string code)
def dummy_currency(code: str) -> Currency:
    return Currency(code)

def test_fx_rate_lookup_error_attributes_and_message():
    ccy1 = dummy_currency("USD")
    ccy2 = dummy_currency("EUR")
    asof = Date(date(2023, 1, 15))
    err = FXRateLookupError(ccy1, ccy2, asof)

    # Check that the attributes are stored correctly
    assert err.ccy1 is ccy1
    assert err.ccy2 is ccy2
    assert err.asof is asof

    # Check that the error message contains the expected parts
    expected_msg = f"Foreign exchange rate for {ccy1}/{ccy2} not found as of {asof}"
    assert str(err) == expected_msg
    assert err.args[0] == expected_msg

def test_fx_rate_lookup_error_inherits_lookup_error():
    ccy1 = dummy_currency("GBP")
    ccy2 = dummy_currency("JPY")
    asof = Date(date(2024, 12, 31))
    err = FXRateLookupError(ccy1, ccy2, asof)

    # Verify inheritance hierarchy
    assert isinstance(err, LookupError)
    assert isinstance(err, Exception)

def test_fx_rate_lookup_error_with_boundary_date():
    ccy1 = dummy_currency("AUD")
    ccy2 = dummy_currency("CAD")
    # Use a very early date to test boundary handling
    asof = Date(date(1900, 1, 1))
    err = FXRateLookupError(ccy1, ccy2, asof)

    # Ensure the message correctly reflects the boundary date
    assert "1900-01-01" in str(err)
    # The message should still follow the same format
    assert str(err).startswith(f"Foreign exchange rate for {ccy1}/{ccy2} not found as of")
