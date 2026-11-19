import datetime
import decimal
import pytest
from pypara.dcc import dcfc_act_365_f

def test_zero_fraction_when_start_equals_asof():
    """When start and asof are the same date, the fraction should be zero."""
    start = datetime.date(2024, 1, 15)
    asof = start
    end = datetime.date(2024, 12, 31)
    result = dcfc_act_365_f(start, asof, end)
    assert result == decimal.Decimal(0), "Fraction should be zero when start == asof"

def test_leap_year_fractions():
    """Verify correct fractions for dates around a leap day."""
    start = datetime.date(2020, 2, 28)
    asof = datetime.date(2020, 2, 29)  # leap day
    end = datetime.date(2020, 3, 1)
    # Actual days between start and asof is 1, so fraction = 1/365
    expected = decimal.Decimal(1) / decimal.Decimal(365)
    assert dcfc_act_365_f(start, asof, end) == expected

    # Asof one day after leap day
    asof2 = datetime.date(2020, 3, 1)
    # Actual days between start and asof2 is 2, so fraction = 2/365
    expected2 = decimal.Decimal(2) / decimal.Decimal(365)
    assert dcfc_act_365_f(start, asof2, end) == expected2

def test_negative_day_count_when_asof_before_start():
    """If asof is before start, the function returns a negative fraction."""
    start = datetime.date(2025, 5, 10)
    asof = datetime.date(2025, 5, 5)  # before start
    end = datetime.date(2025, 6, 1)
    # Actual days between start and asof is -5
    expected = decimal.Decimal(-5) / decimal.Decimal(365)
    assert dcfc_act_365_f(start, asof, end) == expected
