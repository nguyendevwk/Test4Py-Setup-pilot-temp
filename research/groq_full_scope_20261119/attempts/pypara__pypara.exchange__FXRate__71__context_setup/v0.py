import datetime
import pytest
from decimal import Decimal

from pypara.exchange import FXRate
from pypara.currencies import Currencies
from pypara.commons.numbers import ONE, ZERO


def test_fxrate_of_success_and_inversion(tmp_path):
    """Test normal creation via `of` and the inversion operator."""
    eur = Currencies["EUR"]
    usd = Currencies["USD"]
    today = datetime.date.today()
    rate = FXRate.of(eur, usd, today, Decimal("2.0"))
    assert isinstance(rate, FXRate)
    assert rate.ccy1 == eur
    assert rate.ccy2 == usd
    assert rate.date == today
    assert rate.value == Decimal("2.0")

    inverted = ~rate
    assert inverted.ccy1 == usd
    assert inverted.ccy2 == eur
    assert inverted.date == today
    assert inverted.value == Decimal("0.5")


def test_fxrate_of_same_currency_and_value():
    """Creating a rate with identical currencies must have value one."""
    eur = Currencies["EUR"]
    today = datetime.date.today()
    rate = FXRate.of(eur, eur, today, ONE)
    assert rate.value == ONE
    with pytest.raises(ValueError, match="must be `one`"):
        FXRate.of(eur, eur, today, Decimal("1.5"))


def test_fxrate_of_invalid_inputs():
    """Test that invalid arguments raise the correct errors."""
    eur = Currencies["EUR"]
    usd = Currencies["USD"]
    today = datetime.date.today()

    # Wrong type for ccy1
    with pytest.raises(ValueError, match="CCY/1 must be of type `Currency`"):
        FXRate.of("EUR", usd, today, Decimal("1.0"))

    # Wrong type for ccy2
    with pytest.raises(ValueError, match="CCY/2 must be of type `Currency`"):
        FXRate.of(eur, "USD", today, Decimal("1.0"))

    # Value <= zero
    with pytest.raises(ValueError, match="can not be equal to or less than `zero`"):
        FXRate.of(eur, usd, today, ZERO)

    # Wrong type for value (int instead of Decimal)
    with pytest.raises(ValueError, match="FX rate value must be of type `Decimal`"):
        FXRate.of(eur, usd, today, 1)

    # Wrong type for date (int instead of date)
    with pytest.raises(ValueError, match="FX rate date must be of type `date`"):
        FXRate.of(eur, usd, 1, Decimal("1.0"))
