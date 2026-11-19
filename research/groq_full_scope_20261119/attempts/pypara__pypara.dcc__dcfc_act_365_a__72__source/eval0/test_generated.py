import datetime
import pytest
from decimal import Decimal

from pypara.dcc import dcfc_act_365_a


def test_normal_fraction_non_leap_year():
    """
    Verify that the day count fraction for a period that does not cross a leap day
    matches the expected value computed manually.
    """
    start = datetime.date(2021, 1, 1)
    asof = datetime.date(2021, 7, 1)  # 181 days
    expected = Decimal(181) / Decimal(365)
    result = dcfc_act_365_a(start, asof, asof)
    assert result == expected, f"Expected {expected}, got {result}"


def test_leap_year_fraction_crossing_leap_day():
    """
    Verify that the day count fraction correctly uses 366 as the denominator
    when the period includes a leap day.
    """
    start = datetime.date(2020, 12, 31)  # 2020 is a leap year
    asof = datetime.date(2021, 1, 1)     # includes Feb 29, 2020
    # Days between start and asof: 1 day
    expected = Decimal(1) / Decimal(366)
    result = dcfc_act_365_a(start, asof, asof)
    assert result == expected, f"Expected {expected}, got {result}"


def test_fraction_when_start_equals_asof():
    """
    Verify that when the start date equals the asof date, the fraction is zero.
    """
    start = datetime.date(2022, 5, 15)
    asof = datetime.date(2022, 5, 15)
    expected = Decimal(0)
    result = dcfc_act_365_a(start, asof, asof)
    assert result == expected, f"Expected {expected}, got {result}"
