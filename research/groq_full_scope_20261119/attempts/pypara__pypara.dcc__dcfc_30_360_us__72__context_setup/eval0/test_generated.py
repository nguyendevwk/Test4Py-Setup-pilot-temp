import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_30_360_us


def test_normal_case_example_1():
    """Test the example from the docstring (normal case)."""
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 28)
    result = dcfc_30_360_us(start=start, asof=asof, end=asof)
    assert result == Decimal("0.16666666666667")


def test_last_day_of_month_adjustment():
    """Test that the function correctly adjusts dates that are the last day of a month."""
    # Start on 31 Jan, asof on 31 Mar (both last days of month)
    start = datetime.date(2020, 1, 31)
    asof = datetime.date(2020, 3, 31)
    result = dcfc_30_360_us(start=start, asof=asof, end=asof)
    # d1 becomes 30, d2 becomes 30, nod = (30-30)+30*(3-1)+360*0 = 60
    assert result == Decimal("0.16666666666667")


def test_negative_fraction_when_start_after_asof():
    """Test that the function returns a non‑positive fraction when start > asof."""
    start = datetime.date(2021, 1, 1)
    asof = datetime.date(2020, 12, 31)
    result = dcfc_30_360_us(start=start, asof=asof, end=asof)
    # d1=1, d2=31, nod = (31-1)+30*(12-1)+360*(-1) = 30+330-360 = 0
    assert result == Decimal("0")
