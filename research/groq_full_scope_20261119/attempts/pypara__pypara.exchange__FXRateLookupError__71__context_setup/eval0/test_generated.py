import pytest
from datetime import date
from pypara.exchange import FXRateLookupError
from pypara.currencies import Currency

def test_fx_rate_lookup_error_attributes_and_message():
    """Ensure the error stores currencies and date and formats the message correctly."""
    ccy1 = Currency("USD")
    ccy2 = Currency("EUR")
    asof = date(2023, 12, 31)
    err = FXRateLookupError(ccy1, ccy2, asof)

    # Attributes should be stored exactly
    assert err.ccy1 is ccy1
    assert err.ccy2 is ccy2
    assert err.asof == asof

    # Message should contain all parts
    expected_msg = f"Foreign exchange rate for {ccy1}/{ccy2} not found as of {asof}"
    assert str(err) == expected_msg
    assert err.args[0] == expected_msg

def test_fx_rate_lookup_error_with_different_currencies():
    """Different currency instances should be reflected in the error message."""
    ccy1 = Currency("GBP")
    ccy2 = Currency("JPY")
    asof = date(2024, 1, 1)
    err = FXRateLookupError(ccy1, ccy2, asof)

    assert err.ccy1 == ccy1
    assert err.ccy2 == ccy2
    assert err.asof == asof
    assert "GBP/JPY" in str(err)
    assert "2024-01-01" in str(err)

def test_fx_rate_lookup_error_inherits_lookup_error():
    """The exception should be a subclass of LookupError and behave accordingly."""
    ccy1 = Currency("AUD")
    ccy2 = Currency("CAD")
    asof = date(2025, 6, 15)
    err = FXRateLookupError(ccy1, ccy2, asof)

    # Check subclass relationship
    assert isinstance(err, LookupError)
    # Raising the error should propagate as a LookupError
    with pytest.raises(LookupError) as excinfo:
        raise err
    assert excinfo.value is err
