import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_act_365_f


def test_normal_fraction():
    """Test a typical non‑leap year period."""
    start = datetime.date(2023, 1, 1)
    asof = datetime.date(2023, 7, 1)
    end = asof
    fraction = dcfc_act_365_f(start, asof, end)
    # 181 days between Jan 1 and Jul 1 in 2023
    expected = Decimal(181) / Decimal(365)
    assert fraction == expected
    assert fraction < 1, "Fraction should be less than 1 for a partial period"


def test_leap_year_fraction():
    """Test a period that spans a leap day."""
    start = datetime.date(2020, 2, 28)
    asof = datetime.date(2020, 3, 1)
    end = asof
    fraction = dcfc_act_365_f(start, asof, end)
    # 2 days including Feb 29
    expected = Decimal(2) / Decimal(365)
    assert fraction == expected
    # Ensure the function correctly counts the leap day
    assert fraction > Decimal(1) / Decimal(365)


def test_frequency_argument_ignored():
    """Ensure that the optional freq argument does not alter the result."""
    start = datetime.date(2021, 5, 15)
    asof = datetime.date(2021, 6, 15)
    end = asof
    fraction_with_freq = dcfc_act_365_f(start, asof, end, freq=Decimal(12))
    fraction_without_freq = dcfc_act_365_f(start, asof, end)
    assert fraction_with_freq == fraction_without_freq
    assert fraction_with_freq == Decimal(31) / Decimal(365)
