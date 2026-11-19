import datetime
import decimal
import pytest
from pypara.dcc import dcfc_30_360_german

def test_normal_case_example_1():
    """Verify the example from the docstring for a typical February period."""
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 28)
    end = asof
    result = dcfc_30_360_german(start, asof, end)
    assert isinstance(result, decimal.Decimal)
    assert result == decimal.Decimal('0.16666666666667')

def test_boundary_case_last_day_of_month():
    """Check that dates on the last day of a month are treated as day 30."""
    # Start on 31st January, asof on 31st March, end on 31st March
    start = datetime.date(2023, 1, 31)
    asof = datetime.date(2023, 3, 31)
    end = asof
    # Manual calculation:
    # d1 = 30 (31st -> 30), d2 = 30 (31st -> 30)
    # nod = (30-30) + 30*(3-1) + 360*(2023-2023) = 60
    expected = decimal.Decimal('60') / decimal.Decimal('360')
    assert dcfc_30_360_german(start, asof, end) == expected

def test_asof_before_start_returns_zero_fraction():
    """When asof is before start, the fraction should be zero (handled by DCC logic)."""
    # The function itself does not guard this, but the DCC wrapper does.
    # We directly call the function to confirm it still returns a Decimal.
    start = datetime.date(2024, 5, 10)
    asof = datetime.date(2024, 5, 5)   # before start
    end = datetime.date(2024, 6, 10)
    result = dcfc_30_360_german(start, asof, end)
    # The calculation will produce a negative nod, but the DCC wrapper would return ZERO.
    # Here we just ensure the function returns a Decimal and the value is negative.
    assert isinstance(result, decimal.Decimal)
    assert result < decimal.Decimal('0')
