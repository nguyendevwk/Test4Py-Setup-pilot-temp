import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_nl_365


def test_normal_fraction_example_1():
    """Test the standard example from the docstring."""
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 28)
    result = dcfc_nl_365(start=start, asof=asof, end=asof)
    assert isinstance(result, Decimal)
    assert round(result, 14) == Decimal("0.16986301369863")


def test_leap_day_boundary_example_2():
    """Test that the leap day is correctly excluded in the fraction."""
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 29)  # 2008 is a leap year
    result = dcfc_nl_365(start=start, asof=asof, end=asof)
    assert isinstance(result, Decimal)
    # The fraction should be identical to the non‑leap example
    assert round(result, 14) == Decimal("0.16986301369863")


def test_negative_fraction_when_start_after_asof():
    """Test that the function returns a negative fraction when start > asof."""
    start = datetime.date(2023, 5, 1)
    asof = datetime.date(2023, 4, 1)
    result = dcfc_nl_365(start=start, asof=asof, end=asof)
    assert isinstance(result, Decimal)
    # The day count should be negative
    assert result < 0
    # The magnitude should equal the positive fraction for the reversed dates
    reversed_result = dcfc_nl_365(start=asof, asof=start, end=start)
    assert result == -reversed_result
