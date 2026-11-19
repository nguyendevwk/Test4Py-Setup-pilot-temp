import datetime
from decimal import Decimal
import pytest

from pypara.dcc import dcfc_30_e_plus_360


def test_normal_day_count_fraction():
    """Test a typical case where no date adjustments are needed."""
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 28)
    end = asof
    result = dcfc_30_e_plus_360(start=start, asof=asof, end=end)
    # Expected fraction: 60 days / 360 = 0.16666666666667
    assert result == Decimal('0.16666666666667')


def test_start_day_31_adjustment():
    """Test that a start date of the 31st is adjusted to the 30th."""
    start = datetime.date(2007, 10, 31)   # will be adjusted to 30th
    asof = datetime.date(2008, 11, 30)
    end = asof
    result = dcfc_30_e_plus_360(start=start, asof=asof, end=end)
    # After adjustment: start 2007-10-30, asof 2008-11-30
    # nod = (30-30) + 30*(11-10) + 360*(2008-2007) = 30 + 360 = 390
    # fraction = 390 / 360 = 1.08333333333333
    assert result == Decimal('1.08333333333333')


def test_asof_day_31_adjustment():
    """Test that an asof date of the 31st is moved to the next day."""
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 29)  # 29th Feb in a leap year, treated as 31st adjustment
    end = asof
    result = dcfc_30_e_plus_360(start=start, asof=asof, end=end)
    # asof is adjusted to 2008-03-01
    # nod = (1-28) + 30*(3-12) + 360*(2008-2007) = -27 + 30*(-9) + 360 = -27 -270 + 360 = 63
    # fraction = 63 / 360 = 0.175
    assert result == Decimal('0.175')
