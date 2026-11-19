import datetime
from decimal import Decimal
import pytest
from pypara.dcc import DCC, _last_payment_date, _next_payment_date
from pypara.monetary import Money
from pypara.currencies import Currency

# Helper fraction method: simple ACT/365
def act_365(start: datetime.date, asof: datetime.date, end: datetime.date, freq: Decimal | None = None) -> Decimal:
    return Decimal((asof - start).days) / Decimal(365)

def test_calculate_fraction_normal_and_boundary():
    dcc = DCC(
        name="ACT/365",
        altnames=set(),
        currencies=set(),
        calculate_fraction_method=act_365,
    )
    start = datetime.date(2023, 1, 1)
    asof = datetime.date(2023, 6, 1)
    end = datetime.date(2023, 12, 31)
    # Normal case
    frac = dcc.calculate_fraction(start, asof, end)
    assert frac == Decimal(151) / Decimal(365)
    # Boundary: asof before start
    frac_before = dcc.calculate_fraction(datetime.date(2023, 6, 1), datetime.date(2023, 5, 31), end)
    assert frac_before == Decimal(0)
    # Boundary: asof after end
    frac_after = dcc.calculate_fraction(start, datetime.date(2024, 1, 1), end)
    assert frac_after == Decimal(0)

def test_calculate_daily_fraction_edge_cases():
    dcc = DCC(
        name="ACT/365",
        altnames=set(),
        currencies=set(),
        calculate_fraction_method=act_365,
    )
    start = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 12, 31)
    # asof is start date
    asof_start = datetime.date(2023, 1, 1)
    daily_start = dcc.calculate_daily_fraction(start, asof_start, end)
    assert daily_start == Decimal(0)  # asof_minus_1 < start -> yfact=0, tfact=0
    # asof is middle of year
    asof_mid = datetime.date(2023, 6, 15)
    daily_mid = dcc.calculate_daily_fraction(start, asof_mid, end)
    # Should equal 1/365
    assert daily_mid == Decimal(1) / Decimal(365)
    # asof is end date
    asof_end = datetime.date(2023, 12, 31)
    daily_end = dcc.calculate_daily_fraction(start, asof_end, end)
    assert daily_end == Decimal(1) / Decimal(365)

def test_interest_and_coupon_calculation():
    dcc = DCC(
        name="ACT/365",
        altnames=set(),
        currencies=set(),
        calculate_fraction_method=act_365,
    )
    principal = Money(Decimal("1000.00"), Currency("USD"))
    rate = Decimal("0.05")  # 5% annual
    start = datetime.date(2023, 1, 1)
    asof = datetime.date(2023, 6, 1)
    end = datetime.date(2023, 12, 31)
    # Interest accrual
    interest = dcc.interest(principal, rate, start, asof, end)
    expected_frac = Decimal((asof - start).days) / Decimal(365)
    assert interest == principal * rate * expected_frac
    # Coupon calculation: frequency 2 (semiannual), eom None
    coupon = dcc.coupon(principal, rate, start, asof, end, freq=2)
    # prevdate should be 2023-01-01, nextdate 2023-07-01
    prevdate = _last_payment_date(start, asof, 2)
    nextdate = _next_payment_date(prevdate, 2)
    assert prevdate == datetime.date(2023, 1, 1)
    assert nextdate == datetime.date(2023, 7, 1)
    # Coupon interest should equal interest from prevdate to asof
    expected_coupon_frac = Decimal((asof - prevdate).days) / Decimal(365)
    assert coupon == principal * rate * expected_coupon_frac
