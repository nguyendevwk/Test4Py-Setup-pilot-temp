import pytest
from pypara.exchange import FXRateLookupError
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date

def test_fx_rate_lookup_error_attributes_and_message():
    """Verify that the error stores the currencies and date and formats the message."""
    ccy1 = Currency("USD")
    ccy2 = Currency("EUR")
    asof = Date(2023, 12, 31)
    err = FXRateLookupError(ccy1, ccy2, asof)

    # Attributes should be stored correctly
    assert err.ccy1 is ccy1
    assert err.ccy2 is ccy2
    assert err.asof is asof

    # Message should contain the string representations of the inputs
    expected_msg = f"Foreign exchange rate for {ccy1}/{ccy2} not found as of {asof}"
    assert str(err) == expected_msg
    assert err.args[0] == expected_msg

def test_fx_rate_lookup_error_inherits_lookup_error():
    """Ensure the exception is a subclass of LookupError."""
    ccy1 = Currency("GBP")
    ccy2 = Currency("JPY")
    asof = Date(2024, 1, 1)
    err = FXRateLookupError(ccy1, ccy2, asof)

    # The exception should be caught by LookupError
    with pytest.raises(LookupError):
        raise err

    # And also by the base Exception class
    with pytest.raises(Exception):
        raise err

def test_fx_rate_lookup_error_with_same_currency_and_invalid_date():
    """Test edge cases: same currency pair and a date that is not a valid calendar date."""
    # Same currency pair
    ccy = Currency("AUD")
    asof = Date(2025, 2, 28)
    err_same = FXRateLookupError(ccy, ccy, asof)
    assert err_same.ccy1 is ccy and err_same.ccy2 is ccy
    assert f"{ccy}/{ccy}" in str(err_same)

    # Invalid date: Date should raise ValueError if month > 12 or day > 31
    with pytest.raises(ValueError):
        Date(2025, 13, 1)
