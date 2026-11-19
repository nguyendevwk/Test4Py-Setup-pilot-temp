import datetime
import pytest
from decimal import Decimal

from pypara.dcc import dcfc_act_act_icma


def test_normal_fraction():
    """Verify that the fraction is computed correctly for a typical period."""
    start = datetime.date(2019, 3, 2)
    asof = datetime.date(2019, 9, 10)
    end = datetime.date(2020, 3, 2)
    result = dcfc_act_act_icma(start=start, asof=asof, end=end)
    # The expected value is taken from the module's doctest.
    assert result == Decimal('0.5245901639')


def test_zero_fraction_when_start_equals_asof():
    """When the asof date equals the start date, the fraction should be zero."""
    start = datetime.date(2021, 1, 1)
    asof = start
    end = datetime.date(2021, 12, 31)
    result = dcfc_act_act_icma(start=start, asof=asof, end=end)
    assert result == Decimal('0')


def test_zero_division_error_with_zero_freq():
    """Providing a frequency of zero should raise a ZeroDivisionError."""
    start = datetime.date(2020, 1, 1)
    asof = datetime.date(2020, 6, 1)
    end = datetime.date(2020, 12, 31)
    with pytest.raises(ZeroDivisionError):
        dcfc_act_act_icma(start=start, asof=asof, end=end, freq=Decimal('0'))
