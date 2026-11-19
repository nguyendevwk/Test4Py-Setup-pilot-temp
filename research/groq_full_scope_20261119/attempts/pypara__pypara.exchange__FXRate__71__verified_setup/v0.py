import datetime
import pytest
from decimal import Decimal

from pypara.exchange import FXRate
from pypara.currencies import Currencies
from pypara.commons.numbers import ONE, ZERO


def test_fxrate_of_normal_creation_and_properties():
    """Test that FXRate.of creates a valid instance and its properties are correct."""
    today = datetime.date.today()
    rate = FXRate.of(Currencies["EUR"], Currencies["USD"], today, Decimal("2.5"))
    assert isinstance(rate, FXRate)
    assert rate.ccy1 == Currencies["EUR"]
    assert rate.ccy2 == Currencies["USD"]
    assert rate.date == today
    assert rate.value == Decimal("2.5")
    # NamedTuple indexing works
    assert rate[0] == Currencies["EUR"]
    assert rate[1] == Currencies["USD"]
    assert rate[2] == today
    assert rate[3] == Decimal("2.5")


def test_fxrate_inversion_and_consistency():
    """Test that the inversion operator returns the reciprocal rate with swapped currencies."""
    today = datetime.date.today()
    original = FXRate.of(Currencies["GBP"], Currencies["JPY"], today, Decimal("150"))
    inverted = ~original
    assert inverted.ccy1 == Currencies["JPY"]
    assert inverted.ccy2 == Currencies["GBP"]
    assert inverted.date == today
    # Value should be reciprocal
    assert inverted.value == Decimal("150") ** -1
    # Inverting again should give back the original
    double_inverted = ~inverted
    assert double_inverted == original


def test_fxrate_of_invalid_inputs_raises_value_error():
    """Test that FXRate.of raises ValueError for invalid arguments."""
    today = datetime.date.today()
    # Value <= zero
    with pytest.raises(ValueError, match="FX rate value can not be equal to or less than `zero`"):
        FXRate.of(Currencies["EUR"], Currencies["USD"], today, Decimal("-1"))
    # Same currency but value != one
    with pytest.raises(ValueError, match="FX rate to the same currency must be `one`"):
        FXRate.of(Currencies["EUR"], Currencies["EUR"], today, Decimal("1.5"))
    # Wrong type for ccy1
    with pytest.raises(ValueError, match="CCY/1 must be of type `Currency`"):
        FXRate.of("EUR", Currencies["USD"], today, Decimal("2"))
    # Wrong type for ccy2
    with pytest.raises(ValueError, match="CCY/2 must be of type `Currency`"):
        FXRate.of(Currencies["EUR"], "USD", today, Decimal("2"))
    # Wrong type for date
    with pytest.raises(ValueError, match="FX rate date must be of type `date`"):
        FXRate.of(Currencies["EUR"], Currencies["USD"], "2023-01-01", Decimal("2"))
    # Wrong type for value
    with pytest.raises(ValueError, match="FX rate value must be of type `Decimal`"):
        FXRate.of(Currencies["EUR"], Currencies["USD"], today, 2)
