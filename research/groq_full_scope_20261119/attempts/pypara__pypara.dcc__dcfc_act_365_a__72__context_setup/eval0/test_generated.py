import datetime
import decimal
import pytest
from pypara.dcc import dcfc_act_365_a

def test_normal_fraction_with_leap_year():
    """Test a typical period that includes a leap day."""
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 29)  # 2008 is a leap year
    end = asof
    result = dcfc_act_365_a(start, asof, end)
    # Expected fraction: 61 days / 366
    expected = decimal.Decimal(61) / decimal.Decimal(366)
    assert result == expected
    assert result == pytest.approx(decimal.Decimal('0.1666666666666666666666666667'), rel=1e-12)

def test_boundary_fraction_no_leap_day():
    """Test a period that ends exactly on the last day of a non‑leap year."""
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 28)  # 2008 is a leap year but asof is before Feb 29
    end = asof
    result = dcfc_act_365_a(start, asof, end)
    # Expected fraction: 60 days / 365
    expected = decimal.Decimal(60) / decimal.Decimal(365)
    assert result == expected
    assert result == pytest.approx(decimal.Decimal('0.1643835616438356164383561644'), rel=1e-12)

def test_error_fraction_with_invalid_dates():
    """Test that the function handles an invalid date range by returning 0."""
    start = datetime.date(2024, 5, 1)
    asof = datetime.date(2024, 4, 30)  # asof before start
    end = datetime.date(2024, 6, 1)
    result = dcfc_act_365_a(start, asof, end)
    # The implementation does not explicitly check order, but the fraction should be 0
    # because the day count is negative and division by 365/366 yields 0.
    assert result == decimal.Decimal(0)
