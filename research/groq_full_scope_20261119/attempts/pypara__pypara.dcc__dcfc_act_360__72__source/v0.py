import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_act_360


def test_normal_day_count_fraction():
    """
    Verify that the function returns the expected fraction for a typical period.
    """
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 28)
    end = asof
    result = dcfc_act_360(start=start, asof=asof, end=end)
    # The expected value is taken from the doctest example.
    expected = Decimal('0.17222222222222')
    assert result == expected, f"Expected {expected}, got {result}"


def test_zero_length_period():
    """
    When start, asof, and end are the same, the fraction should be zero.
    """
    d = datetime.date(2024, 1, 1)
    result = dcfc_act_360(start=d, asof=d, end=d)
    assert result == Decimal('0'), f"Zero-length period should yield 0, got {result}"


def test_frequency_argument_is_ignored():
    """
    The optional freq argument should not affect the calculation.
    """
    start = datetime.date(2023, 6, 15)
    asof = datetime.date(2023, 7, 15)
    end = asof
    # Compute with freq=None and with a non-zero freq
    result_default = dcfc_act_360(start=start, asof=asof, end=end)
    result_with_freq = dcfc_act_360(start=start, asof=asof, end=end, freq=Decimal('1.5'))
    assert result_default == result_with_freq, (
        f"Frequency argument should be ignored: {result_default} != {result_with_freq}"
    )
