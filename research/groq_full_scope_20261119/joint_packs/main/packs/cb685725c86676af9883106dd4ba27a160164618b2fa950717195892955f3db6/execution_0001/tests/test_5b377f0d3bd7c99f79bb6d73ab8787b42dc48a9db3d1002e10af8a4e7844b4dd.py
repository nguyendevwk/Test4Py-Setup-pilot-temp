import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_act_act


def test_act_act_non_leap_year_fraction():
    """
    Verify that the day count fraction for a period entirely within a non‑leap year
    matches the expected value computed manually.
    """
    start = datetime.date(2023, 1, 1)
    asof = datetime.date(2023, 7, 1)  # 181 days
    end = asof
    # 181 / 365 = 0.4958904109589041
    expected = Decimal(181) / Decimal(365)
    result = dcfc_act_act(start, asof, end)
    assert result == expected
    assert result < Decimal(1)


def test_act_act_leap_year_fraction():
    """
    Verify that the day count fraction correctly accounts for a leap year.
    The period spans from 2020‑02‑01 to 2020‑03‑01 (29 days in a leap year).
    """
    start = datetime.date(2020, 2, 1)
    asof = datetime.date(2020, 3, 1)  # 29 days
    end = asof
    # 29 / 366 = 0.07936507936507936
    expected = Decimal(29) / Decimal(366)
    result = dcfc_act_act(start, asof, end)
    assert result == expected
    assert result < Decimal(1)


def test_act_act_cross_year_boundary():
    """
    Test a period that crosses a leap year boundary.
    From 2019‑12‑31 to 2020‑01‑02 spans 2 days: 1 day in 2019 (non‑leap) and 1 day in 2020 (leap).
    """
    start = datetime.date(2019, 12, 31)
    asof = datetime.date(2020, 1, 2)
    end = asof
    # 1/365 + 1/366
    expected = Decimal(1) / Decimal(365) + Decimal(1) / Decimal(366)
    result = dcfc_act_act(start, asof, end)
    assert result == expected
    assert result < Decimal(1)
