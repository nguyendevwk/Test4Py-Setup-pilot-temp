import datetime
import decimal
import pytest
from pypara.dcc import dcfc_30_360_us

def test_normal_case():
    """Verify the day‑count fraction for a typical 30/360 US calculation."""
    start = datetime.date(2007, 12, 28)
    asof  = datetime.date(2008, 2, 28)
    result = dcfc_30_360_us(start=start, asof=asof, end=asof)
    # Expected value from the docstring example
    assert result == decimal.Decimal('0.1666666666666666666666666667')

def test_boundary_last_day_of_month():
    """Check handling when start and asof are the last day of February."""
    start = datetime.date(2020, 2, 29)   # leap year last day
    asof  = datetime.date(2020, 2, 29)
    result = dcfc_30_360_us(start=start, asof=asof, end=asof)
    # For a single day in a leap year, the fraction should be 1/360
    assert result == decimal.Decimal('0.0027777777777777777777777778')

def test_invalid_input_type():
    """Passing a non‑date type should raise a TypeError."""
    with pytest.raises(TypeError):
        dcfc_30_360_us(start="2021-01-01", asof="2021-01-02", end="2021-01-02")
