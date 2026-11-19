import datetime
import calendar
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_act_365_l


def test_fraction_with_non_leap_year():
    """Fraction should use 365 days in a non‑leap year."""
    start = datetime.date(2023, 1, 1)
    asof = datetime.date(2023, 7, 1)
    end = datetime.date(2023, 12, 31)
    # Actual days between start and asof
    actual_days = (asof - start).days
    expected = Decimal(actual_days) / Decimal(365)
    result = dcfc_act_365_l(start, asof, end)
    assert result == expected
    assert result == pytest.approx(expected, rel=1e-12)


def test_fraction_with_leap_year():
    """Fraction should use 366 days in a leap year."""
    start = datetime.date(2024, 1, 1)
    asof = datetime.date(2024, 7, 1)
    end = datetime.date(2024, 12, 31)
    actual_days = (asof - start).days
    expected = Decimal(actual_days) / Decimal(366)
    result = dcfc_act_365_l(start, asof, end)
    assert result == expected
    assert result == pytest.approx(expected, rel=1e-12)
    # Verify that the year is indeed leap
    assert calendar.isleap(asof.year)


def test_fraction_with_zero_days():
    """When start and asof are the same, the fraction should be zero."""
    start = datetime.date(2025, 5, 15)
    asof = datetime.date(2025, 5, 15)
    end = datetime.date(2025, 12, 31)
    result = dcfc_act_365_l(start, asof, end)
    assert result == Decimal(0)
