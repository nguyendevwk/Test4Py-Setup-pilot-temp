import datetime
from decimal import Decimal
import pytest

from pypara.dcc import dcfc_30_e_360

def test_normal_fraction_calculation():
    """Verify the day count fraction for a typical 30E/360 period."""
    start = datetime.date(2023, 1, 15)
    asof  = datetime.date(2023, 4, 15)
    end   = asof
    # Expected nod = (15-15) + 30*(4-1) + 360*(0) = 90
    expected = Decimal(90) / Decimal(360)
    assert dcfc_30_e_360(start, asof, end) == expected

def test_day_31_adjustment():
    """Check that a start or asof date of the 31st is adjusted to the 30th."""
    start = datetime.date(2023, 1, 31)   # should become 30
    asof  = datetime.date(2023, 2, 28)
    end   = asof
    # nod = (28-30) + 30*(2-1) = -2 + 30 = 28
    expected = Decimal(28) / Decimal(360)
    assert dcfc_30_e_360(start, asof, end) == expected

    start = datetime.date(2023, 1, 15)
    asof  = datetime.date(2023, 2, 31)   # should become 30
    end   = asof
    # nod = (30-15) + 30*(2-1) = 15 + 30 = 45
    expected = Decimal(45) / Decimal(360)
    assert dcfc_30_e_360(start, asof, end) == expected

def test_negative_nod_and_fraction_zero():
    """When asof is before start, nod becomes negative and fraction is negative."""
    start = datetime.date(2023, 5, 10)
    asof  = datetime.date(2023, 4, 10)   # before start
    end   = asof
    # nod = (10-10) + 30*(4-5) = -30
    expected = Decimal(-30) / Decimal(360)
    assert dcfc_30_e_360(start, asof, end) == expected
