import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_act_365_a


def test_normal_act_365_a_fraction():
    """
    Test that the function returns the expected fraction for a typical period
    that does not cross a leap day.
    """
    start = datetime.date(2021, 1, 1)
    asof = datetime.date(2021, 7, 1)
    end = datetime.date(2021, 12, 31)

    # 181 days from 2021-01-01 to 2021-07-01 (exclusive of start)
    actual_days = (asof - start).days
    expected = Decimal(actual_days) / Decimal(365)
    result = dcfc_act_365_a(start, asof, end)

    assert result == expected
    assert result == pytest.approx(Decimal('0.4958904109589041'), rel=1e-14)


def test_leap_day_inclusion():
    """
    Test that the function uses 366 as the denominator when the period
    includes a leap day.
    """
    start = datetime.date(2020, 1, 1)   # 2020 is a leap year
    asof = datetime.date(2020, 3, 1)
    end = datetime.date(2020, 12, 31)

    # 60 days from 2020-01-01 to 2020-03-01
    actual_days = (asof - start).days
    expected = Decimal(actual_days) / Decimal(366)
    result = dcfc_act_365_a(start, asof, end)

    assert result == expected
    assert result == pytest.approx(Decimal('0.1639344262295082'), rel=1e-14)


def test_negative_period_returns_negative_fraction():
    """
    Test that the function correctly handles a period where the asof date
    is before the start date, resulting in a negative day count fraction.
    """
    start = datetime.date(2022, 6, 1)
    asof = datetime.date(2022, 5, 1)  # asof before start
    end = datetime.date(2022, 12, 31)

    # Negative days: -31
    actual_days = (asof - start).days
    expected = Decimal(actual_days) / Decimal(365)
    result = dcfc_act_365_a(start, asof, end)

    assert result == expected
    assert result == pytest.approx(Decimal('-0.0849315068493151'), rel=1e-14)
