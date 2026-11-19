import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_act_act


def test_act_act_normal_period():
    """
    Test a normal non‑leap year period where the asof date is before the end date.
    """
    start = datetime.date(2021, 1, 1)
    asof = datetime.date(2021, 6, 30)
    end = datetime.date(2021, 12, 31)

    result = dcfc_act_act(start=start, asof=asof, end=end)
    # The period from 2021‑01‑01 to 2021‑06‑30 is 180 days in a non‑leap year.
    expected = Decimal(180) / Decimal(365)
    assert result == expected, f"Expected {expected}, got {result}"


def test_act_act_leap_year_boundary():
    """
    Test a period that spans a leap year boundary to ensure leap days are counted correctly.
    """
    start = datetime.date(2019, 12, 31)
    asof = datetime.date(2020, 1, 1)  # 2020 is a leap year
    end = datetime.date(2020, 12, 31)

    result = dcfc_act_act(start=start, asof=asof, end=end)
    # Only one day in the leap year, so fraction should be 1/366
    expected = Decimal(1) / Decimal(366)
    assert result == expected, f"Expected {expected}, got {result}"


def test_act_act_with_none_frequency():
    """
    Verify that passing None for the optional frequency argument does not alter the result.
    """
    start = datetime.date(2022, 3, 1)
    asof = datetime.date(2022, 3, 1)
    end = datetime.date(2022, 3, 1)

    result_with_none = dcfc_act_act(start=start, asof=asof, end=end, freq=None)
    result_without_freq = dcfc_act_act(start=start, asof=asof, end=end)

    assert result_with_none == result_without_freq, (
        f"Result with freq=None ({result_with_none}) should equal result without freq ({result_without_freq})"
    )
    # The fraction for zero days should be zero.
    assert result_with_none == Decimal(0), f"Expected 0, got {result_with_none}"
