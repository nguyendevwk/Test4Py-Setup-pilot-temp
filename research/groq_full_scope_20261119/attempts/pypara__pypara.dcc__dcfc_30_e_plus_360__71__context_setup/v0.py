import datetime
import decimal
import pytest
from pypara.dcc import dcfc_30_e_plus_360

def test_normal_fraction_calculation():
    """Test a typical case where dates are within the same month."""
    start = datetime.date(2023, 1, 15)
    asof = datetime.date(2023, 2, 15)
    end = asof
    result = dcfc_30_e_plus_360(start, asof, end)
    # 30 days difference, so fraction should be 30/360 = 0.083333...
    assert result == decimal.Decimal('0.08333333333333333333333333333')

def test_day_31_adjustment_and_end_of_month():
    """Test that a start date of the 31st is adjusted to the 30th and
    that an asof date of the 31st is moved to the next day."""
    start = datetime.date(2023, 1, 31)   # should become 2023-01-30
    asof = datetime.date(2023, 2, 28)    # asof day 28, no adjustment
    end = asof
    result = dcfc_30_e_plus_360(start, asof, end)
    # nod = (28-30) + 30*(2-1) = -2 + 30 = 28
    assert result == decimal.Decimal('0.07777777777777777777777777778')

    # Test asof adjustment: asof is 31st
    asof31 = datetime.date(2023, 2, 28) + datetime.timedelta(days=1)  # 2023-03-01
    result2 = dcfc_30_e_plus_360(start, asof31, asof31)
    # nod = (1-30) + 30*(3-1) = -29 + 60 = 31
    assert result2 == decimal.Decimal('0.08611111111111111111111111111')

def test_negative_fraction_for_invalid_date_order():
    """When asof is before start, the function should return a negative fraction."""
    start = datetime.date(2023, 5, 10)
    asof = datetime.date(2023, 4, 10)  # earlier than start
    end = asof
    result = dcfc_30_e_plus_360(start, asof, end)
    # nod = (10-10) + 30*(4-5) = 0 - 30 = -30
    assert result == decimal.Decimal('-0.08333333333333333333333333333')
