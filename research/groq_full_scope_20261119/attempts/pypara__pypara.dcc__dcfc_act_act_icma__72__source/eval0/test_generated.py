import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_act_act_icma


def test_normal_case_example():
    """Test the example from the docstring."""
    start = datetime.date(2019, 3, 2)
    asof = datetime.date(2019, 9, 10)
    end = datetime.date(2020, 3, 2)
    result = dcfc_act_act_icma(start=start, asof=asof, end=end)
    assert isinstance(result, Decimal)
    assert round(result, 10) == Decimal("0.5245901639")


def test_boundary_case_same_dates():
    """When start, asof, and end are the same, the fraction should be 1."""
    d = datetime.date(2023, 1, 1)
    result = dcfc_act_act_icma(start=d, asof=d, end=d)
    assert isinstance(result, Decimal)
    assert result == Decimal("1")


def test_frequency_override():
    """Providing a frequency should divide the fraction accordingly."""
    start = datetime.date(2022, 1, 1)
    asof = datetime.date(2022, 7, 1)
    end = datetime.date(2023, 1, 1)
    freq = Decimal("2")  # e.g., semi‑annual
    result = dcfc_act_act_icma(start=start, asof=asof, end=end, freq=freq)
    # Compute expected manually: actual days from start to asof / actual days from start to end / freq
    from pypara.dcc import _get_actual_day_count  # internal helper used by the function
    expected = Decimal(_get_actual_day_count(start, asof)) / Decimal(_get_actual_day_count(start, end)) / freq
    assert isinstance(result, Decimal)
    assert result == expected
