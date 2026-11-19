import datetime
import pytest
from decimal import Decimal

from pypara.currencies import Currencies, Currency
from pypara.exchange import FXRate
from pypara.commons.numbers import ONE, ZERO


def test_fxrate_of_normal_and_invert(tmp_path):
    """Test normal creation via `of` and the inversion operator."""
    eur = Currencies["EUR"]
    usd = Currencies["USD"]
    today = datetime.date.today()
    rate = FXRate.of(eur, usd, today, Decimal("2.0"))
    assert isinstance(rate, FXRate)
    assert rate.ccy1 is eur
    assert rate.ccy2 is usd
    assert rate.date == today
    assert rate.value == Decimal("2.0")

    inverted = ~rate
    assert inverted.ccy1 is usd
    assert inverted.ccy2 is eur
    assert inverted.date == today
    assert inverted.value == Decimal("0.5")  # 1 / 2.0


def test_fxrate_of_boundary_and_self_rate(tmp_path):
    """Test boundary conditions: zero value, same currency with value one."""
    eur = Currencies["EUR"]
    today = datetime.date.today()

    # Value must be > 0
    with pytest.raises(ValueError, match="FX rate value can not be equal to or less than `zero`"):
        FXRate.of(eur, Currencies["USD"], today, Decimal("0"))

    # Same currency must have value one
    with pytest.raises(ValueError, match="FX rate to the same currency must be `one`"):
        FXRate.of(eur, eur, today, Decimal("1.5"))


def test_fxrate_of_invalid_types(tmp_path):
    """Test that invalid argument types raise ValueError."""
    eur = Currencies["EUR"]
    today = datetime.date.today()

    # ccy1 not a Currency
    with pytest.raises(ValueError, match="CCY/1 must be of type `Currency`"):
        FXRate.of("EUR", Currencies["USD"], today, Decimal("2"))

    # ccy2 not a Currency
    with pytest.raises(ValueError, match="CCY/2 must be of type `Currency`"):
        FXRate.of(eur, "USD", today, Decimal("2"))

    # value not a Decimal
    with pytest.raises(ValueError, match="FX rate value must be of type `Decimal`"):
        FXRate.of(eur, Currencies["USD"], today, 2)

    # date not a date
    with pytest.raises(ValueError, match="FX rate date must be of type `date`"):
        FXRate.of(eur, Currencies["USD"], "2023-01-01", Decimal("2"))
