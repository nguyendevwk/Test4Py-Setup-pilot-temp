import datetime
import pytest
from decimal import Decimal

# Import the target function from the package
from pypara.dcc import dcfc_30_e_360

def test_normal_day_count_fraction():
    """
    Verify the day count fraction for a typical period where no dates are 31st.
    """
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 28)
    end = asof  # end is unused in the calculation but required by signature
    result = dcfc_30_e_360(start=start, asof=asof, end=end)
    # Expected value from the docstring example
    expected = Decimal('0.16666666666667')
    assert result == expected, f"Expected {expected}, got {result}"

def test_boundary_day_adjustment():
    """
    Verify that dates falling on the 31st are adjusted to the 30th before calculation.
    """
    start = datetime.date(2007, 10, 31)   # should be treated as 30th
    asof = datetime.date(2008, 11, 30)    # already 30th
    end = asof
    result = dcfc_30_e_360(start=start, asof=asof, end=end)
    # Manual calculation: (30-30) + 30*(11-10) + 360*(2008-2007) = 0 + 30 + 360 = 390
    # Fraction = 390 / 360 = 1.08333333333333
    expected = Decimal('1.08333333333333')
    assert result == expected, f"Expected {expected}, got {result}"

def test_negative_day_count_fraction():
    """
    Verify that the function correctly handles an asof date earlier than the start date,
    resulting in a negative day count fraction.
    """
    start = datetime.date(2008, 3, 15)
    asof = datetime.date(2008, 2, 15)  # earlier than start
    end = asof
    result = dcfc_30_e_360(start=start, asof=asof, end=end)
    # Manual calculation: (15-15) + 30*(2-3) + 360*(2008-2008) = 0 - 30 + 0 = -30
    # Fraction = -30 / 360 = -0.08333333333333
    expected = Decimal('-0.08333333333333')
    assert result == expected, f"Expected {expected}, got {result}"
