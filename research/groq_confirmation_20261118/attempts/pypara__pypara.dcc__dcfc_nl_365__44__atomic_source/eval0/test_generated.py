import datetime
import pytest
from decimal import Decimal

from pypara.dcc import dcfc_nl_365

# --------------------------------------------------------------------------- #
# Test 1: Normal calculation (non‑leap year, no adjustment)
# --------------------------------------------------------------------------- #
def test_dcfc_nl_365_normal():
    start = datetime.date(2023, 1, 1)
    asof  = datetime.date(2023, 7, 1)   # 181 days
    end   = asof
    result = dcfc_nl_365(start, asof, end)
    # 181 / 365 = 0.495890410958904
    assert result == Decimal('0.495890410958904')
    # Ensure the result is a Decimal and within expected bounds
    assert isinstance(result, Decimal)
    assert 0 <= result <= 1

# --------------------------------------------------------------------------- #
# Test 2: Leap day adjustment (start and asof span a leap day)
# --------------------------------------------------------------------------- #
def test_dcfc_nl_365_leap_day_adjustment():
    start = datetime.date(2020, 2, 28)   # 2020 is a leap year
    asof  = datetime.date(2020, 3, 1)    # spans Feb 29
    end   = asof
    # Actual days = 2 (Feb 28, Feb 29, Mar 1 exclusive)
    # Leap day adjustment subtracts 1
    # Result = (2 - 1) / 365 = 1/365
    result = dcfc_nl_365(start, asof, end)
    assert result == Decimal('0.002739726027397')
    # Verify that the adjustment occurs only when a leap day is included
    start_no_leap = datetime.date(2021, 2, 28)
    asof_no_leap  = datetime.date(2021, 3, 1)
    result_no_leap = dcfc_nl_365(start_no_leap, asof_no_leap, asof_no_leap)
    assert result_no_leap == Decimal('0.005479452054794')

# --------------------------------------------------------------------------- #
# Test 3: Error handling – passing non‑date objects
# --------------------------------------------------------------------------- #
def test_dcfc_nl_365_invalid_input():
    start = "2023-01-01"  # string instead of date
    asof  = datetime.date(2023, 7, 1)
    end   = asof
    with pytest.raises(AttributeError):
        # The function will attempt to access date attributes, raising AttributeError
        dcfc_nl_365(start, asof, end)
