import datetime
from decimal import Decimal
import pytest

from pypara.dcc import dcfc_act_360


def test_normal_fraction():
    """Test a typical Act/360 calculation with a non‑leap year period."""
    start = datetime.date(2020, 1, 15)
    asof = datetime.date(2020, 4, 15)  # 91 days
    end = asof
    result = dcfc_act_360(start, asof, end)
    expected = Decimal(91) / Decimal(360)
    assert result == expected
    assert result == pytest.approx(Decimal('0.2527777777777777777777777778'))


def test_leap_year_boundary():
    """Test that the function correctly handles a leap day in the period."""
    start = datetime.date(2019, 12, 31)
    asof = datetime.date(2020, 2, 29)  # 31 + 29 = 60 days
    end = asof
    result = dcfc_act_360(start, asof, end)
    expected = Decimal(60) / Decimal(360)
    assert result == expected
    assert result == pytest.approx(Decimal('0.1666666666666666666666666667'))


def test_negative_fraction_when_asof_before_start():
    """Test that a negative fraction is returned when asof precedes start."""
    start = datetime.date(2021, 5, 1)
    asof = datetime.date(2021, 4, 1)  # 30 days earlier
    end = asof
    result = dcfc_act_360(start, asof, end)
    expected = Decimal(-30) / Decimal(360)
    assert result == expected
    assert result < Decimal(0)
