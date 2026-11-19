import datetime
from decimal import Decimal, getcontext

import pytest

from pypara.dcc import dcfc_act_365_a

# Increase precision for comparison
getcontext().prec = 28


def test_non_leap_year_fraction():
    """
    Test a typical non‑leap year period where the day count fraction
    should be calculated using 365 days in the denominator.
    """
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 28)
    expected = Decimal('0.16986301369863')
    result = dcfc_act_365_a(start, asof, asof)
    assert result == pytest.approx(expected, rel=1e-14), f"Expected {expected}, got {result}"


def test_leap_year_fraction():
    """
    Test a period that spans a leap day. The denominator should be 366.
    """
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 29)  # 2008 is a leap year
    expected = Decimal('0.17213114754098')
    result = dcfc_act_365_a(start, asof, asof)
    assert result == pytest.approx(expected, rel=1e-14), f"Expected {expected}, got {result}"


def test_zero_length_period():
    """
    Test a zero‑length period where start and asof are the same day.
    The fraction should be zero regardless of the denominator.
    """
    start = datetime.date(2024, 5, 15)
    asof = datetime.date(2024, 5, 15)
    result = dcfc_act_365_a(start, asof, asof)
    assert result == Decimal('0'), f"Zero‑length period should yield 0, got {result}"
