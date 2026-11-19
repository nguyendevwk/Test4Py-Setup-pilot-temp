import datetime
from decimal import Decimal
import pytest
from pypara.dcc import DCC
from pypara.currencies import Currency
from pypara.monetary import Money
from pypara.commons.numbers import ONE, ZERO

# Helper calculation method: simple day count as number of days between dates
def simple_days(start: datetime.date, asof: datetime.date, end: datetime.date, freq: Decimal | None = None) -> Decimal:
    return Decimal((asof - start).days)

def test_calculate_fraction_valid_and_invalid_dates():
    """Test that calculate_fraction returns correct fraction for valid dates and zero for invalid."""
    dcc = DCC(
        name="Simple",
        altnames=set(),
        currencies=set(),
        calculate_fraction_method=simple_days
    )
    start = datetime.date(2023, 1, 1)
    asof = datetime.date(2023, 1, 10)
    end = datetime.date(2023, 1, 20)
    # Valid range: start <= asof <= end
    assert dcc.calculate_fraction(start, asof, end) == Decimal(9)
    # asof before start
    assert dcc.calculate_fraction(start, datetime.date(2022, 12, 31), end) == ZERO
    # asof after end
    assert dcc.calculate_fraction(start, datetime.date(2023, 1, 21), end) == ZERO

def test_calculate_daily_fraction_edge_cases():
    """Test calculate_daily_fraction handles boundary conditions correctly."""
    dcc = DCC(
        name="Simple",
        altnames=set(),
        currencies=set(),
        calculate_fraction_method=simple_days
    )
    start = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 1, 10)
    # asof at start date: yfact should be zero
    asof = start
    daily = dcc.calculate_daily_fraction(start, asof, end)
    assert daily == Decimal(0)
    # asof one day before start: yfact zero, tfact zero
    asof_before = start - datetime.timedelta(days=1)
    daily_before = dcc.calculate_daily_fraction(start, asof_before, end)
    assert daily_before == ZERO
    # asof in middle: difference of one day
    asof_mid = datetime.date(2023, 1, 5)
    daily_mid = dcc.calculate_daily_fraction(start, asof_mid, end)
    assert daily_mid == Decimal(1)

def test_interest_calculation_with_principal_and_rate():
    """Test that interest calculation uses the fraction correctly."""
    dcc = DCC(
        name="Simple",
        altnames=set(),
        currencies=set(),
        calculate_fraction_method=simple_days
    )
    principal = Money(Decimal('1000'), Currency('USD'))
    rate = Decimal('0.05')  # 5% annual
    start = datetime.date(2023, 1, 1)
    asof = datetime.date(2023, 7, 1)  # 181 days
    # Expected interest: principal * rate * fraction
    expected_fraction = Decimal((asof - start).days)
    expected_interest = principal * rate * expected_fraction
    assert dcc.interest(principal, rate, start, asof) == expected_interest
