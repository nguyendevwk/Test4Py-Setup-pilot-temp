import datetime
from decimal import Decimal
import pytest
from pypara.dcc import DCC, _last_payment_date, _next_payment_date
from pypara.monetary import Money
from pypara.currencies import Currency

# Simple day‑count method: (end - start).days / 365
def simple_method(start: datetime.date, asof: datetime.date, end: datetime.date, freq: Decimal | None = None) -> Decimal:
    return Decimal((end - start).days) / Decimal(365)

@pytest.fixture
def dcc():
    return DCC(
        name="Simple",
        altnames=set(),
        currencies=set(),
        calculate_fraction_method=simple_method,
    )

def test_calculate_fraction_normal(dcc):
    start = datetime.date(2023, 1, 1)
    asof = datetime.date(2023, 6, 1)
    end = datetime.date(2023, 12, 31)
    frac = dcc.calculate_fraction(start, asof, end)
    expected = Decimal((end - start).days) / Decimal(365)
    assert frac == expected
    # boundary: asof equal to start
    assert dcc.calculate_fraction(start, start, end) == expected
    # boundary: asof equal to end
    assert dcc.calculate_fraction(start, end, end) == Decimal((end - start).days) / Decimal(365)

def test_calculate_fraction_error(dcc):
    start = datetime.date(2023, 6, 1)
    asof = datetime.date(2023, 1, 1)  # asof before start
    end = datetime.date(2023, 12, 31)
    assert dcc.calculate_fraction(start, asof, end) == Decimal(0)
    # asof after end
    asof = datetime.date(2024, 1, 1)
    assert dcc.calculate_fraction(start, asof, end) == Decimal(0)

def test_coupon_and_daily_fraction(dcc):
    start = datetime.date(2023, 1, 1)
    asof = datetime.date(2023, 6, 15)
    end = datetime.date(2023, 12, 31)
    principal = Money(Decimal(1000), Currency("USD"))
    rate = Decimal("0.05")
    # coupon calculation
    coupon = dcc.coupon(principal, rate, start, asof, end, freq=2)
    # compute expected manually
    prev = _last_payment_date(start, asof, 2)
    nextd = _next_payment_date(prev, 2)
    expected_frac = dcc.calculate_fraction(prev, asof, nextd)
    expected_coupon = principal * rate * expected_frac
    assert coupon == expected_coupon
    # daily fraction
    daily = dcc.calculate_daily_fraction(start, asof, end)
    # manual calculation
    yfact = dcc.calculate_fraction(start, asof - datetime.timedelta(days=1), end)
    tfact = dcc.calculate_fraction(start, asof, end)
    assert daily == tfact - yfact
