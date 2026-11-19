import datetime
import decimal
import pytest
from pypara.dcc import dcfc_act_360

def test_zero_fraction_when_same_dates():
    """When start, asof, and end are identical, the fraction should be zero."""
    d = datetime.date(2024, 1, 1)
    result = dcfc_act_360(start=d, asof=d, end=d)
    assert isinstance(result, decimal.Decimal)
    assert result == decimal.Decimal('0')

def test_fraction_for_known_period():
    """Verify the fraction for a known period matches the expected value."""
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 28)
    end = asof
    result = dcfc_act_360(start=start, asof=asof, end=end)
    # The expected value is taken from the docstring example
    expected = decimal.Decimal('0.17222222222222')
    # Use rounding to avoid floating point issues
    assert round(result, 14) == expected

def test_fraction_with_leap_day():
    """Test that the function correctly handles a leap day in the period."""
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 29)  # 2008 is a leap year
    end = asof
    result = dcfc_act_360(start=start, asof=asof, end=end)
    expected = decimal.Decimal('0.17500000000000')
    assert round(result, 14) == expected
