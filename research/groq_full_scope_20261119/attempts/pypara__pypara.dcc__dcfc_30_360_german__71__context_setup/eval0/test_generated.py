import datetime
import decimal
import pytest
from pypara.dcc import dcfc_30_360_german

def test_normal_case():
    """Standard case with non‑end‑of‑month dates."""
    start = datetime.date(2023, 1, 15)
    asof  = datetime.date(2023, 4, 15)
    end   = datetime.date(2023, 4, 15)
    result = dcfc_30_360_german(start, asof, end)
    # Expected: 90 days / 360 = 0.25
    assert result == decimal.Decimal('0.25')

def test_leap_year_boundary():
    """Check handling of February 29 in a leap year."""
    start = datetime.date(2020, 2, 29)   # leap day
    asof  = datetime.date(2020, 3, 31)   # end of month
    end   = datetime.date(2020, 3, 31)
    result = dcfc_30_360_german(start, asof, end)
    # start day is 29, but since it's Feb 29 and last day, d1 becomes 30
    # asof day is 31, so d2 becomes 30
    # nod = (30-30)+30*(3-2)+360*(2020-2020) = 30
    # fraction = 30/360 = 0.0833333333333333
    assert result == decimal.Decimal('0.0833333333333333')

def test_invalid_date_order():
    """When start > asof, the function should still compute normally."""
    start = datetime.date(2023, 5, 1)
    asof  = datetime.date(2023, 4, 30)   # asof before start
    end   = datetime.date(2023, 4, 30)
    result = dcfc_30_360_german(start, asof, end)
    # The algorithm does not guard against this; it will compute a negative fraction
    # nod = (30-30)+30*(4-5)+360*(2023-2023) = -30
    # fraction = -30/360 = -0.0833333333333333
    assert result == decimal.Decimal('-0.0833333333333333')
