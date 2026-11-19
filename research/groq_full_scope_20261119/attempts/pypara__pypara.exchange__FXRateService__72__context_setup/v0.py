import pytest
from decimal import Decimal
from pypara.exchange import FXRate
from pypara.currencies import Currencies
from pypara.commons.zeitgeist import Date

def test_fxrate_of_valid_creation():
    """Creating an FXRate with valid arguments should succeed and produce expected values."""
    today = Date.today()
    rate = FXRate.of(Currencies["EUR"], Currencies["USD"], today, Decimal("1.5"))
    assert isinstance(rate, FXRate)
    assert rate.ccy1 == Currencies["EUR"]
    assert rate.ccy2 == Currencies["USD"]
    assert rate.date == today
    assert rate.value == Decimal("1.5")

def test_fxrate_of_invalid_value_and_same_currency():
    """Creating an FXRate with a non‑positive value or same‑currency pair with non‑one value should raise ValueError."""
    today = Date.today()
    with pytest.raises(ValueError, match="FX rate value can not be equal to or less than `zero`"):
        FXRate.of(Currencies["EUR"], Currencies["USD"], today, Decimal("-0.1"))
    with pytest.raises(ValueError, match="FX rate to the same currency must be `one`"):
        FXRate.of(Currencies["EUR"], Currencies["EUR"], today, Decimal("2"))

def test_fxrate_invert_operation():
    """The inversion operator should return a rate with swapped currencies and reciprocal value."""
    today = Date.today()
    original = FXRate.of(Currencies["GBP"], Currencies["JPY"], today, Decimal("150"))
    inverted = ~original
    assert inverted.ccy1 == Currencies["JPY"]
    assert inverted.ccy2 == Currencies["GBP"]
    assert inverted.date == today
    assert inverted.value == Decimal("150") ** -1
