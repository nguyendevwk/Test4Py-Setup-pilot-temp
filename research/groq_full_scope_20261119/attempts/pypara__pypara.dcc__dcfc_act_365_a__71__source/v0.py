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
    # 181/365 = 0.495890410958904
    assert fraction == Decimal('0.495890410958904')
    # Verify that the fraction is positive and less than 1
    assert fraction > 0
    assert fraction < 1


def test_leap_year_boundary():
    """Test a period that includes a leap day; denominator should be 366."""
    start = datetime.date(2020, 12, 31)
    asof = datetime.date(2021, 1, 1)  # 1 day after leap day
    end = asof
    fraction = dcfc_act_365_a(start, asof, end)
    # 1/366 = 0.00273224043715847
    assert fraction == Decimal('0.002732240437158')
    # Ensure that the denominator used is 366 by comparing with 365
    fraction_365 = Decimal(1) / Decimal(365)
    assert fraction < fraction_365


def test_zero_fraction_when_start_equals_asof():
    """When start and asof are the same, the fraction should be zero."""
    start = datetime.date(2024, 5, 15)
    asof = start
    end = asof
    fraction = dcfc_act_365_a(start, asof, end)
    assert fraction == Decimal('0')
    # The function should not raise an exception for this edge case
    assert isinstance(fraction, Decimal)
