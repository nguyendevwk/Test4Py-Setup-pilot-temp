import datetime
import decimal
import pytest
from pypara.dcc import DCC
from pypara.commons.zeitgeist import Date
from pypara.monetary import Money
from pypara.currencies import Currency

# Helper calculate_fraction_method that returns a simple fraction:
def simple_fraction(start: Date, asof: Date, end: Date, freq: decimal.Decimal | None = None) -> decimal.Decimal:
    # Return number of days between asof and end divided by 365
    days = (end - asof).days
    return decimal.Decimal(days) / decimal.Decimal(365)

# Create a dummy currency for testing
dummy_currency = Currency("USD", "US Dollar", 2)

# Instantiate a DCC with the simple method
dcc = DCC(
    name="Simple",
    altnames=set(),
    currencies={dummy_currency},
    calculate_fraction_method=simple_fraction,
)

def test_calculate_fraction_normal():
    """Test normal calculation where dates are in correct order."""
    start = Date(2023, 1, 1)
    asof = Date(2023, 6, 1)
    end = Date(2023, 12, 31)
    frac = dcc.calculate_fraction(start, asof, end)
    expected_days = (end - asof).days
    assert frac == decimal.Decimal(expected_days) / decimal.Decimal(365)

def test_calculate_fraction_boundary_and_error():
    """Test boundary: asof outside range returns ZERO; asof equal to start or end works."""
    start = Date(2023, 1, 1)
    end = Date(2023, 12, 31)

    # asof before start
    asof_before = Date(2022, 12, 31)
    assert dcc.calculate_fraction(start, asof_before, end) == decimal.Decimal(0)

    # asof after end
    asof_after = Date(2024, 1, 1)
    assert dcc.calculate_fraction(start, asof_after, end) == decimal.Decimal(0)

    # asof equal to start
    asof_start = start
    frac_start = dcc.calculate_fraction(start, asof_start, end)
    assert frac_start == decimal.Decimal((end - asof_start).days) / decimal.Decimal(365)

    # asof equal to end
    asof_end = end
    frac_end = dcc.calculate_fraction(start, asof_end, end)
    assert frac_end == decimal.Decimal(0)

def test_interest_and_coupon():
    """Test interest and coupon calculations with a simple principal and rate."""
    principal = Money(1000, dummy_currency)
    rate = decimal.Decimal("0.05")  # 5% annual
    start = Date(2023, 1, 1)
    asof = Date(2023, 7, 1)
    end = Date(2023, 12, 31)

    # Interest should be principal * rate * fraction
    interest = dcc.interest(principal, rate, start, asof, end)
    expected_frac = dcc.calculate_fraction(start, asof, end)
    assert interest == principal * rate * expected_frac

    # Coupon calculation: assume semi‑annual payments (freq=2)
    coupon = dcc.coupon(principal, rate, start, asof, end, freq=2)
    # The coupon should equal the interest calculated above because the period
    # from the previous payment date to asof is the same as the interest period.
    assert coupon == interest
