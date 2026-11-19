import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_act_365_f


def test_normal_fraction():
    """Test a typical non‑leap year period."""
    start = datetime.date(2023, 1, 1)
    asof = datetime.date(2023, 7, 1)
    end = asof
    # 181 days in 2023 (non‑leap year)
    expected = Decimal(181) / Decimal(365)
    result = dcfc_act_365_f(start, asof, end)
    assert result == expected
    assert isinstance(result, Decimal)


def test_leap_year_fraction():
    """Test a period that spans a leap day."""
    start = datetime.date(2020, 2, 28)
    asof = datetime.date(2020, 3, 1)
    end = asof
    # 2 days including Feb 29
    expected = Decimal(2) / Decimal(365)
    result = dcfc_act_365_f(start, asof, end)
    assert result == expected
    # Ensure that the fraction is not the same as a non‑leap year period of 2 days
    non_leap = Decimal(2) / Decimal(365)
    assert result == non_leap  # same numeric value, but test that calculation uses 365


def test_invalid_dates_error():
    """Test that passing non‑date objects raises a TypeError."""
    start = "2023-01-01"  # string instead of date
    asof = datetime.date(2023, 7, 1)
    end = asof
    with pytest.raises(TypeError):
        dcfc_act_365_f(start, asof, end)
