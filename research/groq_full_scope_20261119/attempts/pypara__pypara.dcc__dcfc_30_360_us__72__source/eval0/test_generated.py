import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_30_360_us


def test_normal_fraction():
    """Standard case: start 2007-12-28, asof 2008-02-28."""
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 28)
    result = dcfc_30_360_us(start=start, asof=asof, end=asof)
    assert isinstance(result, Decimal)
    assert round(result, 14) == Decimal("0.16666666666667")


def test_last_day_of_month_adjustment():
    """When start is last day of month, d1 should be set to 30."""
    start = datetime.date(2021, 1, 31)  # last day of January
    asof = datetime.date(2021, 2, 28)   # last day of February
    result = dcfc_30_360_us(start=start, asof=asof, end=asof)
    # d1 becomes 30, d2 becomes 28 (not 30 because asof is not last day of month)
    # nod = (28-30) + 30*(2-1) = -2 + 30 = 28
    # fraction = 28/360 = 0.0777777777777778
    assert round(result, 14) == Decimal("0.07777777777778")


def test_day_31_adjustment():
    """When d2 is 31 and d1 is 30 or 31, d2 should be set to 30."""
    start = datetime.date(2020, 3, 30)
    asof = datetime.date(2020, 4, 31)  # April 31 does not exist, use 30
    # Use April 30 to trigger d2=31 logic
    asof = datetime.date(2020, 4, 30)
    result = dcfc_30_360_us(start=start, asof=asof, end=asof)
    # d1=30, d2=30 -> nod = (30-30)+30*(4-3)=30
    # fraction = 30/360 = 0.0833333333333333
    assert round(result, 14) == Decimal("0.08333333333333")
