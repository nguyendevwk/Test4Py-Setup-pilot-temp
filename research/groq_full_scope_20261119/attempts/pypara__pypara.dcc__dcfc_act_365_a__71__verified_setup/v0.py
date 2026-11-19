import datetime
from decimal import Decimal
import pytest

from pypara.dcc import dcfc_act_365_a


def test_normal_case_non_leap_year():
    """Test a typical non‑leap year period where the denominator is 365."""
    start = datetime.date(2023, 1, 1)
    asof = datetime.date(2023, 7, 1)  # 181 days
    end = asof
    fraction = dcfc_act_365_a(start, asof, end)
    # 181 / 365
    assert fraction == Decimal(181) / Decimal(365)
    # Verify rounding matches expected value
    assert round(fraction, 14) == Decimal('0.49589041095890')


def test_leap_year_boundary():
    """Test a period that includes a leap day, ensuring denominator becomes 366."""
    start = datetime.date(2020, 1, 1)          # 2020 is a leap year
    asof = datetime.date(2020, 3, 1)           # 60 days (including Feb 29)
    end = asof
    fraction = dcfc_act_365_a(start, asof, end)
    # 60 / 366
    assert fraction == Decimal(60) / Decimal(366)
    assert round(fraction, 14) == Decimal('0.16393442622951')


def test_zero_fraction_when_start_equals_asof():
    """When start and asof are the same, the fraction should be zero."""
    start = datetime.date(2024, 5, 15)
    asof = start
    end = asof
    fraction = dcfc_act_365_a(start, asof, end)
    assert fraction == Decimal(0)
    # Ensure the function does not raise on identical dates
    assert isinstance(fraction, Decimal)
