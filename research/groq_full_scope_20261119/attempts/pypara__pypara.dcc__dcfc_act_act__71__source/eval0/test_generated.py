import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_act_act


def test_normal_fraction():
    """Test a typical non‑leap year period."""
    start = datetime.date(2021, 1, 1)
    asof = datetime.date(2021, 7, 1)
    end = asof
    result = dcfc_act_act(start, asof, end)
    # 181 days in 2021 (non‑leap year)
    expected = Decimal(181) / Decimal(365)
    assert result == expected
    assert isinstance(result, Decimal)


def test_leap_year_fraction():
    """Test a period that spans a leap year."""
    start = datetime.date(2019, 12, 31)
    asof = datetime.date(2020, 1, 1)
    end = asof
    result = dcfc_act_act(start, asof, end)
    # 1 day in a leap year
    expected = Decimal(1) / Decimal(366)
    assert result == expected


def test_freq_argument_ignored():
    """Verify that the optional freq argument does not affect the result."""
    start = datetime.date(2022, 3, 1)
    asof = datetime.date(2022, 3, 31)
    end = asof
    result_with_freq = dcfc_act_act(start, asof, end, freq=Decimal(2))
    result_without_freq = dcfc_act_act(start, asof, end)
    assert result_with_freq == result_without_freq
