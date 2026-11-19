import pytest
from decimal import Decimal
from pypara.exchange import FXRate, Currency
from pypara.currencies import Currencies
from pypara.commons.numbers import ONE, ZERO
from pypara.commons.zeitgeist import Date

def test_fxrate_of_valid_creation():
    """Creating a valid FXRate via the `of` factory should succeed and match a direct constructor."""
    today = Date.today()
    rate_direct = FXRate(Currencies["EUR"], Currencies["USD"], today, Decimal("1.5"))
    rate_factory = FXRate.of(Currencies["EUR"], Currencies["USD"], today, Decimal("1.5"))
    assert rate_factory == rate_direct
    assert rate_factory.ccy1 == Currencies["EUR"]
    assert rate_factory.ccy2 == Currencies["USD"]
    assert rate_factory.date == today
    assert rate_factory.value == Decimal("1.5")

def test_fxrate_of_invalid_arguments():
    """The factory should raise ValueError for invalid types and values."""
    today = Date.today()
    with pytest.raises(ValueError, match="CCY/1 must be of type `Currency`"):
        FXRate.of("EUR", Currencies["USD"], today, Decimal("1.0"))
    with pytest.raises(ValueError, match="FX rate value must be of type `Decimal`"):
        FXRate.of(Currencies["EUR"], Currencies["USD"], today, 1.0)
    with pytest.raises(ValueError, match="FX rate value can not be equal to or less than `zero`"):
        FXRate.of(Currencies["EUR"], Currencies["USD"], today, Decimal("-0.1"))
    with pytest.raises(ValueError, match="FX rate to the same currency must be `one`"):
        FXRate.of(Currencies["EUR"], Currencies["EUR"], today, Decimal("2.0"))

def test_fxrate_invert_operation():
    """Inverting an FXRate should produce the reciprocal rate with swapped currencies."""
    today = Date.today()
    original = FXRate(Currencies["GBP"], Currencies["JPY"], today, Decimal("150.0"))
    inverted = ~original
    assert inverted.ccy1 == Currencies["JPY"]
    assert inverted.ccy2 == Currencies["GBP"]
    assert inverted.date == today
    assert inverted.value == Decimal("150.0") ** -1
    # Inverting twice should return the original rate
    double_inverted = ~inverted
    assert double_inverted == original
