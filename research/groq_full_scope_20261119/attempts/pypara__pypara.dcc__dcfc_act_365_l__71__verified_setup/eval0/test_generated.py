import datetime
import calendar
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_act_365_l


def test_normal_day_count_fraction():
    """
    Verify that the function returns the expected fraction for a typical non‑leap year period.
    """
    start = datetime.date(2023, 1, 1)
    asof = datetime.date(2023, 7, 1)
    end = asof  # end is unused in calculation but required by signature
    result = dcfc_act_365_l(start, asof, end)
    # 181 days from Jan 1 to Jul 1 in 2023
    expected = Decimal(181) / Decimal(365)
    assert result == expected
    assert result < Decimal(1)


def test_leap_year_day_count_fraction():
    """
    Verify that the function correctly uses 366 days for a leap year.
    """
    start = datetime.date(2020, 1, 1)
    asof = datetime.date(2020, 3, 1)
    end = asof
    result = dcfc_act_365_l(start, asof, end)
    # 60 days from Jan 1 to Mar 1 in 2020 (leap year)
    expected = Decimal(60) / Decimal(366)
    assert result == expected
    # Ensure the denominator is indeed 366
    assert calendar.isleap(asof.year)


def test_negative_day_count_fraction():
    """
    Verify that the function can produce a negative fraction when the asof date is before the start date.
    """
    start = datetime.date(2023, 12, 31)
    asof = datetime.date(2023, 1, 1)
    end = asof
    result = dcfc_act_365_l(start, asof, end)
    # 365 days difference but negative because asof < start
    expected = Decimal(-365) / Decimal(365)
    assert result == expected
    assert result < Decimal(0)
