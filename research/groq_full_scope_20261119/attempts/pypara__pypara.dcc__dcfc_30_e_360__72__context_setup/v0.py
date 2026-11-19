import datetime
import decimal
import pytest
from pypara.dcc import dcfc_30_e_360

def test_normal_fraction_calculation():
    """Verify that the function returns the expected fraction for a typical period."""
    start = datetime.date(2023, 1, 15)
    asof = datetime.date(2023, 4, 15)
    end = asof
    result = dcfc_30_e_360(start, asof, end)
    # 30 days per month, 3 months = 90 days => 90/360 = 0.25
    assert result == decimal.Decimal('0.25')

def test_start_day_31_adjustment():
    """When the start date is the 31st, it should be adjusted to the 30th."""
    start = datetime.date(2023, 1, 31)   # will be treated as Jan 30
    asof = datetime.date(2023, 2, 28)
    end = asof
    result = dcfc_30_e_360(start, asof, end)
    # days: (28-30)+30*(2-1)= -2+30=28 => 28/360
    assert result == decimal.Decimal('0.0777777777777778')

def test_invalid_date_range_returns_zero():
    """If start > asof, the function should return 0 (Decimal)."""
    start = datetime.date(2023, 5, 1)
    asof = datetime.date(2023, 4, 30)
    end = datetime.date(2023, 6, 1)
    result = dcfc_30_e_360(start, asof, end)
    assert result == decimal.Decimal('0')
