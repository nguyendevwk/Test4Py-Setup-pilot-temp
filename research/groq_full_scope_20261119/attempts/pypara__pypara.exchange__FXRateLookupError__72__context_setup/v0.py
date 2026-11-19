import pytest
from pypara.exchange import FXRateLookupError
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date
from datetime import date


def test_fx_rate_lookup_error_initialization_and_attributes():
    """Verify that the exception stores the provided currencies and date."""
    ccy1 = Currency("USD")
    ccy2 = Currency("EUR")
    asof = Date(date(2023, 1, 15))
    err = FXRateLookupError(ccy1, ccy2, asof)

    assert err.ccy1 is ccy1
    assert err.ccy2 is ccy2
    assert err.asof is asof
    assert isinstance(err, LookupError)


def test_fx_rate_lookup_error_message_format():
    """Check that the error message contains the correct currency pair and date."""
    ccy1 = Currency("GBP")
    ccy2 = Currency("JPY")
    asof = Date(date(2024, 12, 31))
    err = FXRateLookupError(ccy1, ccy2, asof)

    expected_msg = f"Foreign exchange rate for {ccy1}/{ccy2} not found as of {asof}"
    assert str(err) == expected_msg
    assert expected_msg in err.args[0]


def test_fx_rate_lookup_error_inherits_lookup_error_and_is_raised():
    """Ensure that the exception can be raised and caught as a LookupError."""
    ccy1 = Currency("AUD")
    ccy2 = Currency("CAD")
    asof = Date(date(2025, 6, 30))

    with pytest.raises(LookupError) as excinfo:
        raise FXRateLookupError(ccy1, ccy2, asof)

    assert isinstance(excinfo.value, FXRateLookupError)
    assert excinfo.value.ccy1 == ccy1
    assert excinfo.value.ccy2 == ccy2
    assert excinfo.value.asof == asof
