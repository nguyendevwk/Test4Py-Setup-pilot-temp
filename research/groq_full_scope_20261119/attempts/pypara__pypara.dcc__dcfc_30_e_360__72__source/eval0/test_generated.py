import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_30_e_360


def test_normal_fraction_calculation():
    """Verify the day count fraction for a typical period."""
    start = datetime.date(2023, 1, 15)
    asof = datetime.date(2023, 4, 15)
    end = asof  # end is unused in calculation but required by signature
    result = dcfc_30_e_360(start=start, asof=asof, end=end)
    # 30 days per month, 3 months difference => 90 days / 360 = 0.25
    assert result == Decimal("0.25")


def test_day_31_replacement_behavior():
    """Ensure dates with day 31 are replaced with 30 before calculation."""
    start = datetime.date(2023, 1, 31)  # should become 30
    asof = datetime.date(2023, 4, 30)   # remains 30
    end = asof
    result = dcfc_30_e_360(start=start, asof=asof, end=end)
    # Effective start day 30, asof day 30: 0 days difference
    assert result == Decimal("0")


def test_asof_day_31_replacement_and_fraction():
    """Test that asof day 31 is replaced and fraction is computed correctly."""
    start = datetime.date(2023, 2, 28)
    asof = datetime.date(2023, 3, 31)  # should become 30
    end = asof
    result = dcfc_30_e_360(start=start, asof=asof, end=end)
    # Effective asof day 30, start day 28: 2 days difference
    assert result == Decimal("0.0055555555555556")
