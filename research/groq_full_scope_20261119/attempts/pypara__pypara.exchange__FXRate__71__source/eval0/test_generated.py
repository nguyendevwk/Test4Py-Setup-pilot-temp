import datetime
import pytest
from decimal import Decimal

from pypara.exchange import FXRate
from pypara.currencies import Currencies, Currency
from pypara.commons.numbers import ONE, ZERO


def test_normal_fxrate_creation_and_inversion():
    """Normal creation of an FXRate and its inversion."""
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
    assert inverted.value == Decimal("0.4")  # 1 / 2.5


def test_boundary_fxrate_same_currency_and_value_one():
    """FXRate with same currency must have value one."""
    eur = Currencies["EUR"]
    today = datetime.date.today()
    rate = FXRate.of(eur, eur, today, ONE)
    assert rate.ccy1 == eur
    assert rate.ccy2 == eur
    assert rate.value == ONE

    with pytest.raises(ValueError, match="must be `one`"):
        FXRate.of(eur, eur, today, Decimal("1.1"))


def test_error_invalid_arguments_and_value():
    """Invalid types and non‑positive values raise ValueError."""
    eur = Currencies["EUR"]
    usd = Currencies["USD"]
    today = datetime.date.today()

    # Wrong type for ccy1
    with pytest.raises(ValueError, match="CCY/1 must be of type"):
        FXRate.of("EUR", usd, today, Decimal("1.0"))

    # Wrong type for ccy2
    with pytest.raises(ValueError, match="CCY/2 must be of type"):
        FXRate.of(eur, "USD", today, Decimal("1.0"))

    # Non‑positive value
    with pytest.raises(ValueError, match="can not be equal to or less than"):
        FXRate.of(eur, usd, today, ZERO)

    # Wrong type for date
    with pytest.raises(ValueError, match="FX rate date must be of type"):
        FXRate.of(eur, usd, "2023-01-01", Decimal("1.0"))
