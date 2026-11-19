import datetime
import pytest
from decimal import Decimal

# Import the target function from the package
from pypara.dcc import dcfc_30_360_german


def test_normal_day_count_fraction():
    """
    Verify that the function returns the expected fraction for a typical period.
    """
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 28)
    end = asof
    result = dcfc_30_360_german(start=start, asof=asof, end=end)
    # The expected value is derived from the example in the docstring
    assert result == Decimal('0.1666666666666666666666666667')


def test_boundary_day_adjustments():
    """
    Test the boundary conditions where the start or asof dates are the last day of a month
    (31st or February end) and the function should adjust the day to 30.
    """
    # Start on 31st January, asof on 31st March, end on 31st March
    start = datetime.date(2021, 1, 31)
    asof = datetime.date(2021, 3, 31)
    end = asof
    # Manually compute expected nod:
    # d1 = 30 (since start.day == 31)
    # d2 = 30 (asof.day == 31)
    # nod = (30-30) + 30*(3-1) + 360*(2021-2021) = 60
    expected_fraction = Decimal(60) / Decimal(360)
    assert dcfc_30_360_german(start, asof, end) == expected_fraction


def test_invalid_input_raises_attribute_error():
    """
    Passing an object that does not have the required date attributes should raise an AttributeError.
    """
    start = "not a date"
    asof = datetime.date(2021, 3, 15)
    end = asof
    with pytest.raises(AttributeError):
        dcfc_30_360_german(start=start, asof=asof, end=end)
