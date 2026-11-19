import pytest
from pypara.exchange import FXRateLookupError
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date
from datetime import date

def test_fx_rate_lookup_error_attributes_and_message():
    """Verify that the exception stores the currencies and date and formats the message."""
    ccy1 = Currency("USD")
    ccy2 = Currency("EUR")
    asof = Date(date(2023, 1, 15))
    exc = FXRateLookupError(ccy1, ccy2, asof)

    # Attributes should be set correctly
    assert exc.ccy1 is ccy1
    assert exc.ccy2 is ccy2
    assert exc.asof is asof

    # Message should contain the string representations
    expected_msg = f"Foreign exchange rate for {ccy1}/{ccy2} not found as of {asof}"
    assert str(exc) == expected_msg
    assert exc.args[0] == expected_msg

def test_fx_rate_lookup_error_inherits_lookup_error():
    """Ensure the exception is a subclass of LookupError."""
    ccy1 = Currency("GBP")
    ccy2 = Currency("JPY")
    asof = Date(date(2024, 12, 31))
    exc = FXRateLookupError(ccy1, ccy2, asof)

    # The exception should be caught by LookupError
    with pytest.raises(LookupError) as ctx:
        raise exc
    assert ctx.value is exc

def test_fx_rate_lookup_error_with_invalid_inputs():
    """Passing non‑Currency or non‑Date objects should raise TypeError during construction."""
    # The constructor does not perform type checks, but the Currency and Date classes
    # are expected to be used. Passing plain strings should still create an exception
    # but the message will reflect the string representations.
    ccy1 = "USD"          # not a Currency instance
    ccy2 = "EUR"          # not a Currency instance
    asof = "2023-01-01"   # not a Date instance

    exc = FXRateLookupError(ccy1, ccy2, asof)

    # The attributes are stored as provided
    assert exc.ccy1 == ccy1
    assert exc.ccy2 == ccy2
    assert exc.asof == asof

    # The message should use the string representations of the inputs
    expected_msg = f"Foreign exchange rate for {ccy1}/{ccy2} not found as of {asof}"
    assert str(exc) == expected_msg
