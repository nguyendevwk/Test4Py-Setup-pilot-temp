import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_30_360_isda


def test_normal_day_count_fraction():
    """Standard case where no date adjustments are needed."""
    start = datetime.date(2023, 1, 15)
    asof = datetime.date(2023, 4, 15)
    end = asof  # end is unused in calculation but required by signature
    result = dcfc_30_360_isda(start=start, asof=asof, end=end)
    # Expected nod = (15-15) + 30*(4-1) + 360*(0) = 90
    assert result == Decimal(90) / Decimal(360)
    assert result == Decimal('0.25')


def test_boundary_adjustment_start_31_and_asof_31():
    """Test that a start date of the 31st is adjusted to the 30th and
    that an asof date of the 31st is adjusted to the 30th when the start
    day is 30."""
    start = datetime.date(2023, 1, 31)   # should become 30th
    asof = datetime.date(2023, 2, 28)    # no adjustment needed
    end = asof
    result = dcfc_30_360_isda(start=start, asof=asof, end=end)
    # After adjustment: start = 2023-01-30, asof = 2023-02-28
    # nod = (28-30) + 30*(2-1) + 360*0 = -2 + 30 = 28
    assert result == Decimal(28) / Decimal(360)
    assert result == Decimal('0.07777777777778')

    # Now test asof adjustment when start day is 30
    start = datetime.date(2023, 1, 30)
    asof = datetime.date(2023, 2, 31)  # should become 2023-02-30
    end = asof
    result = dcfc_30_360_isda(start=start, asof=asof, end=end)
    # After adjustment: asof = 2023-02-30
    # nod = (30-30) + 30*(2-1) + 360*0 = 30
    assert result == Decimal(30) / Decimal(360)
    assert result == Decimal('0.08333333333333')


def test_invalid_input_type_raises_type_error():
    """Passing a non-date type should raise a TypeError when the function
    attempts to access the .day attribute."""
    start = "2023-01-15"  # string, not a date
    asof = datetime.date(2023, 4, 15)
    end = asof
    with pytest.raises(AttributeError):
        dcfc_30_360_isda(start=start, asof=asof, end=end)
