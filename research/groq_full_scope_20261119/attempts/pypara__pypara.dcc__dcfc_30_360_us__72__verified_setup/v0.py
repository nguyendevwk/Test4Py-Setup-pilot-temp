import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_30_360_us


def test_normal_case():
    """Standard calculation with mid‑month dates."""
    start = datetime.date(2023, 1, 15)
    asof = datetime.date(2023, 4, 15)
    # Expected: 90 days / 360 = 0.25
    result = dcfc_30_360_us(start=start, asof=asof, end=asof)
    assert result == Decimal("0.25")


def test_last_day_of_month_adjustment():
    """When start is the last day of a month, it should be treated as day 30."""
    start = datetime.date(2023, 1, 31)  # last day of January
    asof = datetime.date(2023, 2, 28)   # last day of February
    # d1 becomes 30, d2 becomes 30 (since asof is last day)
    # nod = (30-30)+30*(2-1)+360*(0)=30
    # fraction = 30/360 = 0.083333...
    result = dcfc_30_360_us(start=start, asof=asof, end=asof)
    assert result == Decimal("0.08333333333333333333333333333")


def test_d2_31_with_d1_30_or_31():
    """When d2 is 31 and d1 is 30 or 31, d2 should be set to 30."""
    start = datetime.date(2023, 3, 30)  # d1 = 30
    asof = datetime.date(2023, 4, 31)   # d2 = 31
    # d2 becomes 30, nod = (30-30)+30*(4-3)+360*0 = 30
    result = dcfc_30_360_us(start=start, asof=asof, end=asof)
    assert result == Decimal("0.08333333333333333333333333333")
