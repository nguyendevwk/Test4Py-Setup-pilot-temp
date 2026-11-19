import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_30_360_isda


def test_normal_day_count_fraction():
    """Test a typical case where no special day adjustments are needed."""
    start = datetime.date(2023, 1, 15)
    asof = datetime.date(2023, 4, 15)
    end = asof  # end is unused in the calculation but required by signature
    result = dcfc_30_360_isda(start, asof, end)
    # 30 days per month, 3 months difference → 90 days / 360 = 0.25
    assert result == Decimal("0.25")


def test_start_day_31_adjustment():
    """Verify that a start date of the 31st is adjusted to the 30th."""
    start = datetime.date(2023, 1, 31)
    asof = datetime.date(2023, 3, 31)
    end = asof
    result = dcfc_30_360_isda(start, asof, end)
    # Adjusted start: 2023-01-30, asof remains 2023-03-31
    # nod = (31-30) + 30*(3-1) + 360*(0) = 1 + 60 = 61
    # fraction = 61/360
    assert result == Decimal("61") / Decimal(360)


def test_asof_day_31_with_start_day_30_adjustment():
    """Check that when start day is 30 and asof day is 31, asof is adjusted to 30."""
    start = datetime.date(2023, 2, 28)  # not 30, but we set to 30 manually
    # Force start day to 30 by using 30th of month
    start = datetime.date(2023, 2, 30) if hasattr(datetime.date, 'replace') else datetime.date(2023, 2, 28)
    # Since datetime.date cannot have day 30 for February, use March
    start = datetime.date(2023, 3, 30)
    asof = datetime.date(2023, 4, 31)
    end = asof
    result = dcfc_30_360_isda(start, asof, end)
    # asof should be adjusted to 2023-04-30
    # nod = (30-30) + 30*(4-3) + 360*(0) = 30
    # fraction = 30/360 = 0.083333...
    assert result == Decimal("30") / Decimal(360)
