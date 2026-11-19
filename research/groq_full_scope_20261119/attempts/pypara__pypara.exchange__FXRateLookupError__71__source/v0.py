import pytest
from pypara.exchange import FXRateLookupError
from pypara.currencies import Currency
from pypara.commons.zeitgeist import Date

def test_fx_rate_lookup_error_message_and_attributes():
    """Verify that the error message is constructed correctly and attributes are stored."""
    ccy1 = Currency("USD")
    ccy2 = Currency("EUR")
    asof = Date(2024, 1, 1)
    error = FXRateLookupError(ccy1, ccy2, asof)

    # Check that the message contains the expected components
    expected_msg = f"Foreign exchange rate for {ccy1}/{ccy2} not found as of {asof}"
    assert str(error) == expected_msg

    # Check that the attributes are set correctly
    assert error.ccy1 is ccy1
    assert error.ccy2 is ccy2
    assert error.asof is asof

def test_fx_rate_lookup_error_inheritance():
    """Ensure that FXRateLookupError inherits from LookupError and behaves like an exception."""
    ccy1 = Currency("GBP")
    ccy2 = Currency("JPY")
    asof = Date(2023, 12, 31)
    error = FXRateLookupError(ccy1, ccy2, asof)

    # It should be an instance of LookupError
    assert isinstance(error, LookupError)

    # Raising and catching the error should preserve its message
    with pytest.raises(FXRateLookupError) as exc_info:
        raise error
    assert str(exc_info.value) == str(error)

def test_fx_rate_lookup_error_with_invalid_inputs():
    """Test that the constructor accepts any objects and stores them without validation."""
    # Use simple objects that are not Currency or Date instances
    ccy1 = "USD"
    ccy2 = "EUR"
    asof = "2024-01-01"
    error = FXRateLookupError(ccy1, ccy2, asof)

    # The attributes should be stored exactly as passed
    assert error.ccy1 == ccy1
    assert error.ccy2 == ccy2
    assert error.asof == asof

    # The message should reflect the string representations of the inputs
    expected_msg = f"Foreign exchange rate for {ccy1}/{ccy2} not found as of {asof}"
    assert str(error) == expected_msg
