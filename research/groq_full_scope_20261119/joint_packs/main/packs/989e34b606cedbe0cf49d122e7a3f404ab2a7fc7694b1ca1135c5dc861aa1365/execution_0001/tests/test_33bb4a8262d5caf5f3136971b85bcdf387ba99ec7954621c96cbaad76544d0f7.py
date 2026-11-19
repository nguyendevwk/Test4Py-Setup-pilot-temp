import datetime
import pytest
from decimal import Decimal

from pypara.dcc import dcfc_act_360, _get_actual_day_count


def test_dcfc_act_360_normal_case():
    """Test a typical Act/360 calculation over a non‑leap year period."""
    start = datetime.date(2023, 1, 1)
    asof = datetime.date(2023, 4, 1)
    end = datetime.date(2023, 4, 1)
    # 90 days between start and asof
    expected_fraction = Decimal(90) / Decimal(360)
    result = dcfc_act_360(start, asof, end)
    assert result == expected_fraction, f"Expected {expected_fraction}, got {result}"


def test_dcfc_act_360_boundary_leap_year():
    """Test the calculation across a leap day to ensure the actual day count is correct."""
    start = datetime.date(2020, 2, 28)
    asof = datetime.date(2020, 3, 1)
    end = datetime.date(2020, 3, 1)
    # 2 days: Feb 28 -> Feb 29 (leap day) -> Mar 1
    expected_fraction = Decimal(2) / Decimal(360)
    result = dcfc_act_360(start, asof, end)
    assert result == expected_fraction, f"Expected {expected_fraction}, got {result}"


def test_dcfc_act_360_zero_day_count():
    """Test that the function returns zero when start and asof are the same date."""
    start = datetime.date(2023, 5, 15)
    asof = datetime.date(2023, 5, 15)
    end = datetime.date(2023, 5, 15)
    # No days elapsed
    expected_fraction = Decimal(0) / Decimal(360)
    result = dcfc_act_360(start, asof, end)
    assert result == expected_fraction, f"Expected {expected_fraction}, got {result}"
