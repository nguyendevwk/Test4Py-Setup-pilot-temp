import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_nl_365
from pypara.commons.zeitgeist import Date


def test_normal_day_count_fraction():
    """Test the day count fraction for a typical period including a leap day."""
    start = Date(2007, 12, 28)
    asof = Date(2008, 2, 29)
    end = Date(2008, 2, 29)
    result = dcfc_nl_365(start=start, asof=asof, end=end)
    # Expected value from the docstring example
    expected = Decimal('0.16986301369863')
    assert result == expected, f"Expected {expected}, got {result}"


def test_boundary_leap_year_adjustment():
    """Test that the function correctly subtracts the leap day when the period spans Feb 29."""
    start = Date(2008, 2, 1)
    asof = Date(2009, 5, 31)
    end = Date(2009, 5, 31)
    result = dcfc_nl_365(start=start, asof=asof, end=end)
    expected = Decimal('1.32602739726027')
    assert result == expected, f"Expected {expected}, got {result}"


def test_zero_day_count_when_start_equals_end():
    """When start and end are the same, the day count fraction should be zero."""
    start = Date(2024, 1, 1)
    asof = Date(2024, 1, 1)
    end = Date(2024, 1, 1)
    result = dcfc_nl_365(start=start, asof=asof, end=end)
    assert result == Decimal('0'), f"Expected Decimal('0'), got {result}"
