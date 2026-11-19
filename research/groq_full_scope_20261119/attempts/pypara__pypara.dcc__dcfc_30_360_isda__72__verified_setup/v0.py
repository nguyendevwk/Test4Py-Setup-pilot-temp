import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_30_360_isda


def test_normal_fraction():
    """Standard case where no day adjustments are required."""
    start = datetime.date(2023, 1, 15)
    asof = datetime.date(2023, 4, 15)
    end = asof  # end is unused in calculation but required by signature
    result = dcfc_30_360_isda(start=start, asof=asof, end=end)
    # 30 days per month, 3 months difference => 90 days / 360 = 0.25
    assert result == Decimal("0.25")


def test_start_day_31_adjustment():
    """When the start day is 31, it should be adjusted to 30."""
    start = datetime.date(2023, 1, 31)
    asof = datetime.date(2023, 3, 31)
    end = asof
    result = dcfc_30_360_isda(start=start, asof=asof, end=end)
    # Adjusted start: 2023-01-30, asof: 2023-03-31
    # nod = (31-30) + 30*(3-1) + 360*(0) = 1 + 60 = 61
    # fraction = 61/360
    assert result == Decimal(61) / Decimal(360)


def test_asof_day_31_with_start_30_adjustment():
    """When start day is 30 and asof day is 31, asof should be adjusted to 30."""
    start = datetime.date(2023, 2, 30)  # already 30
    asof = datetime.date(2023, 3, 31)
    end = asof
    result = dcfc_30_360_isda(start=start, asof=asof, end=end)
    # asof adjusted to 2023-03-30
    # nod = (30-30) + 30*(3-2) + 360*0 = 30
    # fraction = 30/360 = 0.083333...
    assert result == Decimal(30) / Decimal(360)
