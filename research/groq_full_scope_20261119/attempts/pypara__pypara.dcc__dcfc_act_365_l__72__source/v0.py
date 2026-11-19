import datetime
import calendar
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_act_365_l


def test_normal_fraction():
    """Test a typical non‑leap year period."""
    start = datetime.date(2023, 1, 1)
    asof = datetime.date(2023, 7, 1)
    end = asof
    result = dcfc_act_365_l(start, asof, end)
    # 181 days from Jan 1 to Jul 1 in a non‑leap year
    expected = Decimal(181) / Decimal(365)
    assert result == expected
    assert result < Decimal(1)


def test_leap_year_fraction():
    """Test that a leap year uses 366 in the denominator."""
    start = datetime.date(2020, 1, 1)
    asof = datetime.date(2020, 7, 1)
    end = asof
    result = dcfc_act_365_l(start, asof, end)
    # 181 days from Jan 1 to Jul 1 in a leap year
    expected = Decimal(181) / Decimal(366)
    assert result == expected
    assert result < Decimal(1)
    # Ensure the denominator is indeed 366
    assert calendar.isleap(asof.year)


def test_frequency_argument_ignored():
    """Verify that the optional freq argument does not influence the result."""
    start = datetime.date(2021, 3, 1)
    asof = datetime.date(2021, 6, 1)
    end = asof
    # Pass a non‑zero frequency
    freq = Decimal('0.5')
    result_with_freq = dcfc_act_365_l(start, asof, end, freq=freq)
    result_without_freq = dcfc_act_365_l(start, asof, end)
    assert result_with_freq == result_without_freq
    # Ensure the result is a Decimal
    assert isinstance(result_with_freq, Decimal)
