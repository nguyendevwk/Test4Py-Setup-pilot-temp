import datetime
from decimal import Decimal
import pytest
from pypara.dcc import DCC
from pypara.commons.zeitgeist import Date
from pypara.currencies import Currency
from pypara.monetary import Money

# Helper: a simple DCC that always returns 1 for any fraction calculation
def one_fraction(start: Date, asof: Date, end: Date, freq: Decimal | None = None) -> Decimal:
    return Decimal(1)

simple_dcc = DCC(
    name="ONE",
    altnames=set(),
    currencies=set(),
    calculate_fraction_method=one_fraction,
)

def test_calculate_fraction_normal_and_boundary():
    start = Date(2024, 1, 1)
    asof = Date(2024, 6, 1)
    end = Date(2024, 12, 31)

    # Normal case: asof within range
    assert simple_dcc.calculate_fraction(start, asof, end) == Decimal(1)

    # Boundary case: asof equals start
    assert simple_dcc.calculate_fraction(start, start, end) == Decimal(1)

    # Boundary case: asof equals end
    assert simple_dcc.calculate_fraction(start, end, end) == Decimal(1)

    # Error case: asof outside range
    before = Date(2023, 12, 31)
    after = Date(2025, 1, 1)
    assert simple_dcc.calculate_fraction(start, before, end) == Decimal(0)
    assert simple_dcc.calculate_fraction(start, after, end) == Decimal(0)

def test_calculate_daily_fraction():
    start = Date(2024, 1, 1)
    end = Date(2024, 12, 31)

    # asof is after start: daily fraction should be 1 - 0 = 1
    asof = Date(2024, 6, 1)
    assert simple_dcc.calculate_daily_fraction(start, asof, end) == Decimal(1)

    # asof is the start date: asof_minus_1 < start, so yfact = 0, tfact = 1
    asof_start = start
    assert simple_dcc.calculate_daily_fraction(start, asof_start, end) == Decimal(1)

    # asof is before start: asof_minus_1 < start, tfact = 0, yfact = 0
    asof_before = Date(2023, 12, 31)
    assert simple_dcc.calculate_daily_fraction(start, asof_before, end) == Decimal(0)

def test_interest_and_coupon_calculation():
    principal = Money(Decimal(1000), Currency("USD"))
    rate = Decimal("0.05")  # 5% annual
    start = Date(2024, 1, 1)
    asof = Date(2024, 6, 1)
    end = Date(2024, 12, 31)

    # Interest: uses calculate_fraction which returns 1
    interest = simple_dcc.interest(principal, rate, start, asof, end)
    assert interest == principal * rate * Decimal(1)

    # Coupon: prevdate is start, nextdate is end (since freq=1 year)
    coupon = simple_dcc.coupon(principal, rate, start, asof, end, freq=1)
    # coupon should equal interest calculated above
    assert coupon == interest
