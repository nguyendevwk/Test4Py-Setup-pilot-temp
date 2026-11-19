import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_30_e_plus_360


def test_normal_day_count_fraction():
    """Test the standard calculation for a typical period."""
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 28)
    end = asof
    result = dcfc_30_e_plus_360(start=start, asof=asof, end=end)
    assert isinstance(result, Decimal)
    assert round(result, 14) == Decimal('0.16666666666667')


def test_start_day_31_adjustment():
    """Verify that a start date of the 31st is adjusted to the 30th."""
    start = datetime.date(2007, 10, 31)  # 31st should become 30th
    asof = datetime.date(2008, 11, 30)
    end = asof
    # Manual calculation: nod = (30-30)+30*(11-10)+360*(2008-2007)=30+360=390
    expected = Decimal(390) / Decimal(360)
    result = dcfc_30_e_plus_360(start=start, asof=asof, end=end)
    assert result == expected


def test_negative_day_count_fraction():
    """Check that the function returns a negative fraction when asof precedes start."""
    start = datetime.date(2008, 3, 1)
    asof = datetime.date(2008, 2, 28)  # earlier than start
    end = asof
    result = dcfc_30_e_plus_360(start=start, asof=asof, end=end)
    # nod should be negative: (28-1)+30*(2-3)+360*(2008-2008)=27-30=-3
    assert result == Decimal(-3) / Decimal(360)
