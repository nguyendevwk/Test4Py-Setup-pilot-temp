import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_nl_365


def test_normal_fraction_with_non_leap_year():
    """
    Verify that the day count fraction for a period that does not include a leap day
    matches the expected value from the documentation examples.
    """
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 28)
    end = asof
    result = dcfc_nl_365(start, asof, end)
    expected = Decimal('0.16986301369863')
    assert result == expected, f"Expected {expected}, got {result}"


def test_leap_day_adjustment():
    """
    Verify that the function correctly subtracts one day when the period includes
    a leap day (Feb 29). The example from the documentation uses Feb 29, 2008.
    """
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 29)
    end = asof
    result = dcfc_nl_365(start, asof, end)
    expected = Decimal('0.16986301369863')
    assert result == expected, f"Expected {expected}, got {result}"


def test_fraction_over_multiple_years_and_leap_years():
    """
    Test a period that spans multiple years, including a leap year, to ensure
    the calculation handles year boundaries correctly.
    """
    start = datetime.date(2007, 10, 31)
    asof = datetime.date(2008, 11, 30)
    end = asof
    result = dcfc_nl_365(start, asof, end)
    expected = Decimal('1.08219178082192')
    assert result == expected, f"Expected {expected}, got {result}"
