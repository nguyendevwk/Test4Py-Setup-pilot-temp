import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_act_act_icma


def test_normal_fraction_computation():
    """Verify that the function returns the expected fraction for a typical period."""
    start = datetime.date(2019, 3, 2)
    asof = datetime.date(2019, 9, 10)
    end = datetime.date(2020, 3, 2)

    result = dcfc_act_act_icma(start=start, asof=asof, end=end)
    # The expected value is taken from the docstring example.
    expected = Decimal("0.5245901639")
    assert result == expected, f"Expected {expected}, got {result}"


def test_boundary_zero_fraction_when_dates_equal():
    """When start, asof and end are the same, the fraction should be zero."""
    d = datetime.date(2023, 1, 1)
    result = dcfc_act_act_icma(start=d, asof=d, end=d)
    assert result == Decimal("0"), "Fraction should be zero when all dates are equal"


def test_fraction_zero_when_asof_out_of_range():
    """If asof is outside the [start, end] interval, the function should return zero."""
    start = datetime.date(2023, 1, 1)
    end = datetime.date(2023, 12, 31)

    # asof before start
    asof_before = datetime.date(2022, 12, 31)
    result_before = dcfc_act_act_icma(start=start, asof=asof_before, end=end)
    assert result_before == Decimal("0"), "Fraction should be zero when asof is before start"

    # asof after end
    asof_after = datetime.date(2024, 1, 1)
    result_after = dcfc_act_act_icma(start=start, asof=asof_after, end=end)
    assert result_after == Decimal("0"), "Fraction should be zero when asof is after end"
