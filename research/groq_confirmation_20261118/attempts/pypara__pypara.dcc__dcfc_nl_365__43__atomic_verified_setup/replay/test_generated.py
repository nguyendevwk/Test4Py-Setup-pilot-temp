import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_nl_365
from pypara.commons.zeitgeist import Date


def test_normal_example_1():
    """Test the example from the docstring where the period includes a leap day."""
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 29)  # leap day
    result = dcfc_nl_365(start=start, asof=asof, end=asof)
    # The expected value is given in the docstring
    assert round(result, 14) == Decimal('0.16986301369863')


def test_boundary_no_leap_day():
    """Test a period that does not include a leap day and where asof equals start."""
    start = datetime.date(2021, 3, 1)
    asof = datetime.date(2021, 3, 1)
    result = dcfc_nl_365(start=start, asof=asof, end=asof)
    # No days elapsed, so fraction should be zero
    assert result == Decimal('0')


def test_end_date_ignored_and_freq_unused():
    """Test that the end date and optional freq argument are ignored by the function."""
    start = datetime.date(2020, 1, 1)
    asof = datetime.date(2020, 6, 30)
    end = datetime.date(2021, 12, 31)  # different from asof
    freq = Decimal('0.5')
    result = dcfc_nl_365(start=start, asof=asof, end=end, freq=freq)
    # Compute expected manually: days between start and asof minus leap day adjustment
    days = (asof - start).days
    # 2020 is a leap year, but Feb 29 is before asof, so subtract 1
    expected = Decimal(days - 1) / Decimal(365)
    assert result == expected
