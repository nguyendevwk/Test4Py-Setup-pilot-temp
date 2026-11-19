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


def test_day_31_adjustment():
    """Ensure dates ending on the 31st are adjusted to the 30th."""
    start = datetime.date(2023, 1, 31)  # should become 30th
    asof = datetime.date(2023, 2, 28)   # unchanged
    end = asof
    result = dcfc_30_e_360(start=start, asof=asof, end=end)
    # Adjusted start: 30th Jan to 28th Feb => 28 days
    assert result == Decimal("0.0777777777777778")  # 28/360


def test_asof_day_31_adjustment_and_boundary():
    """Test adjustment of asof date when it ends on the 31st and a boundary case."""
    start = datetime.date(2023, 1, 15)
    asof = datetime.date(2023, 2, 28)  # unchanged
    end = datetime.date(2023, 3, 31)   # end is unused but provided
    result = dcfc_30_e_360(start=start, asof=asof, end=end)
    # 13 days in Jan (15-31) + 30 days in Feb = 43 days / 360
    assert result == Decimal("0.11944444444444444")
