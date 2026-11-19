import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_act_act


def test_normal_fraction_with_non_leap_year():
    """Test a typical period that does not cross a leap year boundary."""
    start = datetime.date(2021, 1, 1)
    asof = datetime.date(2021, 7, 1)
    end = datetime.date(2021, 12, 31)
    # 181 days in 2021 (non‑leap year)
    expected = Decimal(181) / Decimal(365)
    result = dcfc_act_act(start, asof, end)
    assert result == expected
    assert result == pytest.approx(expected, rel=1e-12)


def test_fraction_across_leap_and_non_leap_years():
    """Test a period that spans a leap year and a non‑leap year."""
    start = datetime.date(2019, 12, 31)
    asof = datetime.date(2020, 12, 31)
    end = datetime.date(2021, 12, 31)
    # 366 days in 2020 (leap year) + 365 days in 2021
    # but only count days up to asof (2020‑12‑31) which is 366 days
    expected = Decimal(366) / Decimal(366)  # 1.0
    result = dcfc_act_act(start, asof, end)
    assert result == expected
    assert result == pytest.approx(expected, rel=1e-12)


def test_fraction_when_asof_equals_start():
    """When asof equals start, the fraction should be zero."""
    start = datetime.date(2022, 3, 15)
    asof = start
    end = datetime.date(2023, 3, 15)
    result = dcfc_act_act(start, asof, end)
    assert result == Decimal(0)
    # Ensure that the function does not raise and handles the zero‑length range
    assert isinstance(result, Decimal)
