import datetime
import calendar
from decimal import Decimal
import pytest

from pypara.dcc import dcfc_act_act

def test_normal_non_leap_year_fraction():
    """Test a typical period that does not cross a leap year boundary."""
    start = datetime.date(2023, 1, 1)
    asof = datetime.date(2023, 6, 30)
    end = datetime.date(2023, 12, 31)
    # All days are in a non‑leap year, so fraction = days / 365
    days = (asof - start).days
    expected = Decimal(days) / Decimal(365)
    result = dcfc_act_act(start, asof, end)
    assert result == expected
    assert result < Decimal('0.5')  # less than half a year

def test_leap_year_boundary_fraction():
    """Test a period that spans a leap year, ensuring leap days are counted correctly."""
    start = datetime.date(2020, 12, 31)   # 2020 is a leap year
    asof = datetime.date(2021, 1, 1)      # next day, crossing the year boundary
    end = datetime.date(2021, 12, 31)
    # 2020 has 366 days, 2021 has 365 days
    # Only one day in 2020 (leap year) and one day in 2021 (non‑leap)
    expected = Decimal(1) / Decimal(366) + Decimal(1) / Decimal(365)
    result = dcfc_act_act(start, asof, end)
    assert result == expected
    # The fraction should be slightly larger than 1/365 because of the leap day
    assert result > Decimal(1) / Decimal(365)

def test_invalid_date_range_returns_zero():
    """When asof is before start, the function should return Decimal(0)."""
    start = datetime.date(2024, 5, 1)
    asof = datetime.date(2024, 4, 30)  # before start
    end = datetime.date(2024, 12, 31)
    result = dcfc_act_act(start, asof, end)
    assert result == Decimal('0')
    # Ensure that the result is not a negative fraction
    assert result >= Decimal('0')
