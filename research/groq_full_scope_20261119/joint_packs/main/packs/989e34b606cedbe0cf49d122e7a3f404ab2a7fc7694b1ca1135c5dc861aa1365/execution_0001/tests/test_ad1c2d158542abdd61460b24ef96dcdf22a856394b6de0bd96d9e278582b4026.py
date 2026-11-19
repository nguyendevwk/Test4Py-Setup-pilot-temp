import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_act_360


def test_dcfc_act_360_normal_case():
    """Test a typical period where the asof is before the end date."""
    start = datetime.date(2023, 1, 1)
    asof = datetime.date(2023, 6, 30)
    end = datetime.date(2023, 12, 31)
    fraction = dcfc_act_360(start, asof, end)
    # Actual days from 2023-01-01 to 2023-06-30 is 180
    assert fraction == Decimal(180) / Decimal(360)
    # The fraction should be exactly 0.5
    assert fraction == Decimal("0.5")


def test_dcfc_act_360_boundary_same_day():
    """When start, asof, and end are the same day, the fraction should be zero."""
    day = datetime.date(2024, 2, 29)
    fraction = dcfc_act_360(day, day, day)
    assert fraction == Decimal(0)
    # The fraction should be exactly 0.0
    assert fraction == Decimal("0.0")


def test_dcfc_act_360_error_asof_before_start():
    """If asof is before start, the function should still compute the fraction based on actual days."""
    start = datetime.date(2023, 5, 1)
    asof = datetime.date(2023, 4, 30)  # asof before start
    end = datetime.date(2023, 5, 31)
    # The function does not guard against asof < start, so it will compute negative days
    fraction = dcfc_act_360(start, asof, end)
    # Days from 2023-05-01 to 2023-04-30 is -1
    assert fraction == Decimal(-1) / Decimal(360)
    # The fraction should be exactly -0.0027777777777778
    assert round(fraction, 14) == Decimal("-0.00277777777778")
