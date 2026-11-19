import datetime
import pytest
from decimal import Decimal

from pypara.exchange import FXRate
from pypara.currencies import Currencies
from pypara.commons.numbers import ONE, ZERO
from pypara.commons.zeitgeist import Date


def test_fxrate_normal_and_invert(tmp_path):
    """Test normal creation via `of` and the inversion operator."""
    eur = Currencies["EUR"]
    usd = Currencies["USD"]
    today = Date(datetime.date.today())

    # Normal creation
    rate = FXRate.of(eur, usd, today, Decimal("2.5"))
    assert rate.ccy1 == eur
    assert rate.ccy2 == usd
    assert rate.date == today
    assert rate.value == Decimal("2.5")

    # Inversion
    inv_rate = ~rate
    assert inv_rate.ccy1 == usd
    assert inv_rate.ccy2 == eur
    assert inv_rate.date == today
    assert inv_rate.value == Decimal("0.4")  # 1 / 2.5 == 0.4


def test_fxrate_boundary_value(tmp_path):
    """Test boundary condition: value must be > 0."""
    eur = Currencies["EUR"]
    usd = Currencies["USD"]
    today = Date(datetime.date.today())

    # Value exactly zero should raise
    with pytest.raises(ValueError, match="FX rate value can not be equal to or less than `zero`"):
        FXRate.of(eur, usd, today, ZERO)

    # Value just above zero should succeed
    rate = FXRate.of(eur, usd, today, Decimal("0.0001"))
    assert rate.value == Decimal("0.0001")


def test_fxrate_error_conditions(tmp_path):
    """Test various error conditions for invalid arguments."""
    eur = Currencies["EUR"]
    usd = Currencies["USD"]
    today = Date(datetime.date.today())

    # Same currency with non-one value
    with pytest.raises(ValueError, match="FX rate to the same currency must be `one`"):
        FXRate.of(eur, eur, today, Decimal("1.1"))

    # Invalid type for ccy1
    with pytest.raises(ValueError, match="CCY/1 must be of type `Currency`"):
        FXRate.of("EUR", usd, today, Decimal("1.0"))

    # Invalid type for ccy2
    with pytest.raises(ValueError, match="CCY/2 must be of type `Currency`"):
        FXRate.of(eur, "USD", today, Decimal("1.0"))

    # Invalid type for value
    with pytest.raises(ValueError, match="FX rate value must be of type `Decimal`"):
        FXRate.of(eur, usd, today, 1.0)

    # Invalid type for date
    with pytest.raises(ValueError, match="FX rate date must be of type `date`"):
        FXRate.of(eur, usd, datetime.date.today(), Decimal("1.0"))
