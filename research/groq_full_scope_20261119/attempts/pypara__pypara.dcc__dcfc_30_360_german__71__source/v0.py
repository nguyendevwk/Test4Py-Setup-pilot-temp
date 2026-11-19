import datetime
import pytest
from decimal import Decimal

# Import the target function from the package
from pypara.dcc import dcfc_30_360_german


def test_normal_day_count_fraction():
    """
    Verify the day count fraction for a typical case using the examples from the docstring.
    """
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 28)
    end = asof
    result = dcfc_30_360_german(start=start, asof=asof, end=end)
    # Expected value from the docstring example
    expected = Decimal('0.16666666666667')
    assert result == expected, f"Expected {expected}, got {result}"


def test_boundary_day_adjustments():
    """
    Test the boundary conditions for dates that are the last day of a month
    or the 31st, ensuring the internal adjustments are applied correctly.
    """
    # Start on 31st January, asof on 31st March, end different from asof
    start = datetime.date(2021, 1, 31)
    asof = datetime.date(2021, 3, 31)
    end = datetime.date(2021, 4, 30)  # end != asof
    result = dcfc_30_360_german(start=start, asof=asof, end=end)
    # d1 should be 30 (31st -> 30), d2 should be 30 (31st -> 30 because end != asof)
    # nod = (30-30) + 30*(3-1) + 360*(2021-2021) = 60
    expected = Decimal('60') / Decimal(360)
    assert result == expected, f"Boundary adjustment failed: expected {expected}, got {result}"

    # Now test February 28 on a non-leap year where asof is the last day of month
    start = datetime.date(2021, 1, 15)
    asof = datetime.date(2021, 2, 28)  # last day of Feb in non-leap year
    end = asof  # end == asof, so d2 should be 28, not 30
    result = dcfc_30_360_german(start=start, asof=asof, end=end)
    # d1 = 15, d2 = 28, nod = (28-15) + 30*(2-1) + 360*0 = 13 + 30 = 43
    expected = Decimal('43') / Decimal(360)
    assert result == expected, f"Feb 28 adjustment failed: expected {expected}, got {result}"


def test_invalid_input_raises_attribute_error():
    """
    Passing an object that does not have the required date attributes should raise an AttributeError.
    """
    class Dummy:
        pass

    start = Dummy()
    asof = Dummy()
    end = Dummy()
    with pytest.raises(AttributeError):
        dcfc_30_360_german(start=start, asof=asof, end=end)
