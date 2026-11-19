import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_30_e_plus_360


def test_normal_case():
    """Standard calculation with no special day adjustments."""
    start = datetime.date(2023, 1, 15)
    asof = datetime.date(2023, 4, 15)
    end = asof  # end is unused in calculation
    result = dcfc_30_e_plus_360(start=start, asof=asof, end=end)
    # 30 days per month, 3 months difference
    expected = Decimal(90) / Decimal(360)
    assert result == expected, f"Expected {expected}, got {result}"


def test_boundary_day_adjustments():
    """Verify that start day 31 is set to 30 and asof day 31 is incremented by one."""
    start = datetime.date(2023, 1, 31)  # should become 30
    asof = datetime.date(2023, 2, 28)   # asof day 28, no increment
    result = dcfc_30_e_plus_360(start=start, asof=asof, end=asof)
    # After adjustment: start=30, asof=28 -> nod = (28-30)+30*(2-1)= -2+30=28
    expected = Decimal(28) / Decimal(360)
    assert result == expected

    # Test asof day 31 increment
    start = datetime.date(2023, 1, 15)
    asof = datetime.date(2023, 2, 28)  # asof day 28, no increment
    result = dcfc_30_e_plus_360(start=start, asof=asof, end=asof)
    expected = Decimal(30) / Decimal(360)
    assert result == expected

    # asof day 31 case
    start = datetime.date(2023, 1, 15)
    asof = datetime.date(2023, 2, 28)  # asof day 28, no increment
    result = dcfc_30_e_plus_360(start=start, asof=asof, end=asof)
    assert result == Decimal(30) / Decimal(360)


def test_negative_day_count_fraction():
    """When asof is earlier than start, the fraction should be negative."""
    start = datetime.date(2023, 5, 15)
    asof = datetime.date(2023, 4, 15)  # earlier month
    result = dcfc_30_e_plus_360(start=start, asof=asof, end=asof)
    # nod = (15-15)+30*(4-5)+360*(0)= -30
    expected = Decimal(-30) / Decimal(360)
    assert result == expected
