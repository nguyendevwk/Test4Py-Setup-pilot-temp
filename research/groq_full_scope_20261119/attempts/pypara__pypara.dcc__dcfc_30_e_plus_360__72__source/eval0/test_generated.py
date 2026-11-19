import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_30_e_plus_360


def test_normal_day_count_fraction():
    """Verify the day count fraction for a typical period."""
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 28)
    end = asof
    result = dcfc_30_e_plus_360(start=start, asof=asof, end=end)
    assert isinstance(result, Decimal)
    assert round(result, 14) == Decimal("0.16666666666667")


def test_boundary_start_day_31_and_asof_end_of_month():
    """Test handling of start day 31 and asof day 31 (roll‑over logic)."""
    start = datetime.date(2007, 10, 31)   # start day 31 should be treated as 30
    asof = datetime.date(2008, 2, 29)     # asof day 29 (not 31)
    end = asof
    result = dcfc_30_e_plus_360(start=start, asof=asof, end=end)
    # Expected nod: (29-30) + 30*(2-10) + 360*(2008-2007) = -1 + 30*(-8) + 360 = -1 -240 + 360 = 119
    assert round(result, 14) == Decimal("0.33055555555556")


def test_negative_day_count_fraction_when_asof_before_start():
    """Ensure that the function returns a negative fraction if asof precedes start."""
    start = datetime.date(2008, 3, 1)
    asof = datetime.date(2008, 2, 28)  # asof before start
    end = asof
    result = dcfc_30_e_plus_360(start=start, asof=asof, end=end)
    assert isinstance(result, Decimal)
    assert result < 0
    # Compute expected nod manually: (28-1) + 30*(2-3) + 360*(2008-2008) = 27 -30 = -3
    assert result == Decimal("-3") / Decimal(360)
