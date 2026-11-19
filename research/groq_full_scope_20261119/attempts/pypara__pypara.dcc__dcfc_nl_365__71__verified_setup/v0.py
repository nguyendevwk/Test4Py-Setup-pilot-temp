import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_nl_365


def test_normal_day_count_fraction():
    """Verify the day count fraction for a typical period."""
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 28)
    end = asof
    result = dcfc_nl_365(start=start, asof=asof, end=end)
    # Expected value from the docstring example
    expected = Decimal('0.16986301369863')
    assert result == expected, f"Expected {expected}, got {result}"


def test_leap_day_adjustment():
    """Ensure that a leap day is correctly subtracted from the count."""
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 29)  # 2008 is a leap year
    end = asof
    result = dcfc_nl_365(start=start, asof=asof, end=end)
    # The same as the non‑leap example, because the leap day is removed
    expected = Decimal('0.16986301369863')
    assert result == expected, f"Expected {expected}, got {result}"


def test_boundary_full_year():
    """Test a period that spans more than one year and includes a leap year."""
    start = datetime.date(2007, 10, 31)
    asof = datetime.date(2008, 11, 30)
    end = asof
    result = dcfc_nl_365(start=start, asof=asof, end=end)
    # Expected value from the docstring example
    expected = Decimal('1.08219178082192')
    assert result == expected, f"Expected {expected}, got {result}"
