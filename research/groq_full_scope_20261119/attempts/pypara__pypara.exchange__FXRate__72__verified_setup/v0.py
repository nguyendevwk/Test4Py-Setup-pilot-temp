import datetime
import pytest
from decimal import Decimal

from pypara.exchange import FXRate
from pypara.currencies import Currencies
from pypara.commons.numbers import ONE, ZERO


def test_fxrate_of_normal_and_invert(tmp_path):
    """Test normal creation via `of` and the inversion operator."""
    eur = Currencies["EUR"]
    usd = Currencies["USD"]
    today = datetime.date.today()
    rate = FXRate.of(eur, usd, today, Decimal("2.5"))
    assert isinstance(rate, FXRate)
    assert rate.ccy1 == eur
    assert rate.ccy2 == usd
    assert rate.date == today
    assert rate.value == Decimal("2.5")

    inverted = ~rate
    assert inverted.ccy1 == usd
    assert inverted.ccy2 == eur
    assert inverted.date == today
    # Inversion should be reciprocal
    assert inverted.value == Decimal("2.5") ** -1
    # Inverting twice returns the original rate
    assert ~inverted == rate


def test_fxrate_of_boundary_and_self_rate(tmp_path):
    """Test boundary conditions: zero value, negative value, same‑currency with value 1."""
    eur = Currencies["EUR"]
    today = datetime.date.today()

    # Value must be > 0
    with pytest.raises(ValueError, match="FX rate value can not be equal to or less than `zero`"):
        FXRate.of(eur, Currencies["USD"], today, ZERO)

    with pytest.raises(ValueError, match="FX rate value can not be equal to or less than `zero`"):
        FXRate.of(eur, Currencies["USD"], today, Decimal("-1"))

    # Same‑currency rate must be 1
    with pytest.raises(ValueError, match="FX rate to the same currency must be `one`"):
        FXRate.of(eur, eur, today, Decimal("1.1"))

    # Valid same‑currency rate of 1
    same_rate = FXRate.of(eur, eur, today, ONE)
    assert same_rate.ccy1 == same_rate.ccy2 == eur
    assert same_rate.value == ONE


def test_fxrate_of_invalid_types(tmp_path):
    """Test that passing wrong types raises ValueError."""
    eur = Currencies["EUR"]
    today = datetime.date.today()

    # Wrong type for ccy1
    with pytest.raises(ValueError, match="CCY/1 must be of type `Currency`"):
        FXRate.of("EUR", Currencies["USD"], today, Decimal("1.2"))

    # Wrong type for ccy2
    with pytest.raises(ValueError, match="CCY/2 must be of type `Currency`"):
        FXRate.of(eur, "USD", today, Decimal("1.2"))

    # Wrong type for date
    with pytest.raises(ValueError, match="FX rate date must be of type `date`"):
        FXRate.of(eur, Currencies["USD"], "2024-01-01", Decimal("1.2"))

    # Wrong type for value
    with pytest.raises(ValueError, match="FX rate value must be of type `Decimal`"):
        FXRate.of(eur, Currencies["USD"], today, 1.2)
