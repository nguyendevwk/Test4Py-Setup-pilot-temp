import datetime
import calendar
from decimal import Decimal
import pytest

from pypara.dcc import dcfc_act_365_l


def test_normal_fraction():
    """Test a typical non‑leap year calculation."""
    start = datetime.date(2023, 1, 1)
    asof = datetime.date(2023, 7, 1)
    end = asof
    # Actual days between start and asof
    actual_days = (asof - start).days
    expected = Decimal(actual_days) / Decimal(365)
    result = dcfc_act_365_l(start, asof, end)
    assert result == expected
    assert result < Decimal('1')
    assert result > Decimal('0')


def test_leap_year_fraction():
    """Test calculation when the asof year is a leap year."""
    start = datetime.date(2020, 1, 1)
    asof = datetime.date(2020, 12, 31)
    end = asof
    actual_days = (asof - start).days
    expected = Decimal(actual_days) / Decimal(366)  # 2020 is a leap year
    result = dcfc_act_365_l(start, asof, end)
    assert result == expected
    assert result < Decimal('1')
    assert result > Decimal('0')


def test_asof_before_start_raises():
    """Ensure that passing an asof date earlier than start raises a ValueError."""
    start = datetime.date(2023, 6, 1)
    asof = datetime.date(2023, 5, 1)  # earlier than start
    end = asof
    with pytest.raises(ValueError):
        # The function will compute a negative day count which is invalid
        dcfc_act_365_l(start, asof, end)
