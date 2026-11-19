import datetime
from decimal import Decimal
import pytest

from pypara.dcc import DCC
from pypara.commons.zeitgeist import Date
from pypara.currencies import Currency
from pypara.monetary import Money
from pypara.commons.numbers import ONE, ZERO


# Helper day count method: simple ACT/365
def act_365(start: Date, asof: Date, end: Date, freq: Decimal | None = None) -> Decimal:
    days = (asof - start).days
    return Decimal(days) / Decimal(365)


def test_calculate_fraction_normal():
    """Normal case: asof between start and end."""
    dcc = DCC(
        name="ACT/365",
        altnames=set(),
        currencies=set(),
        calculate_fraction_method=act_365,
    )
    start = Date(2024, 1, 1)
    asof = Date(2024, 4, 1)  # 90 days after start
    end = Date(2024, 12, 31)
    frac = dcc.calculate_fraction(start, asof, end)
    assert frac == Decimal(90) / Decimal(365)


def test_calculate_fraction_boundary():
    """Boundary case: asof equals start."""
    dcc = DCC(
        name="ACT/365",
        altnames=set(),
        currencies=set(),
        calculate_fraction_method=act_365,
    )
    start = Date(2024, 1, 1)
    asof = start
    end = Date(2024, 12, 31)
    frac = dcc.calculate_fraction(start, asof, end)
    assert frac == ZERO


def test_interest_calculation():
    """Interest accrual using DCC."""
    dcc = DCC(
        name="ACT/365",
        altnames=set(),
        currencies=set(),
        calculate_fraction_method=act_365,
    )
    principal = Money(Decimal("1000.00"), Currency("USD"))
    rate = Decimal("0.05")  # 5% annual
    start = Date(2024, 1, 1)
    asof = Date(2024, 7, 1)  # 181 days
    interest = dcc.interest(principal, rate, start, asof)
    expected = principal * rate * Decimal(181) / Decimal(365)
    assert interest == expected
