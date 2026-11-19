import datetime
from decimal import Decimal

from pypara.dcc import dcfc_30_360_us


def test_zero_fraction_for_identical_dates():
    """When start, asof and end are the same, the day count fraction should be zero."""
    start = datetime.date(2023, 5, 15)
    asof = datetime.date(2023, 5, 15)
    end = datetime.date(2023, 5, 15)
    result = dcfc_30_360_us(start=start, asof=asof, end=end)
    assert result == Decimal(0)


def test_last_day_of_month_adjustments():
    """Verify that the function correctly adjusts dates that fall on the last day of a month."""
    # Start on last day of February (non‑leap year)
    start = datetime.date(2023, 2, 28)
    # Asof on last day of April
    asof = datetime.date(2023, 4, 30)
    # End is the same as asof
    end = asof
    # Expected calculation:
    # d1 = 30 (adjusted from 28 because it's last day of month)
    # d2 = 30 (already 30)
    # nod = (30-30) + 30*(4-2) + 360*(0) = 60
    # fraction = 60 / 360 = 0.166666666666666666...
    expected = Decimal(60) / Decimal(360)
    result = dcfc_30_360_us(start=start, asof=asof, end=end)
    assert result == expected


def test_day_count_fraction_with_31st_and_end_of_month():
    """Test the special handling of 31st days and end‑of‑month dates."""
    # Start on 31st January
    start = datetime.date(2023, 1, 31)
    # Asof on 31st March (not last day of month)
    asof = datetime.date(2023, 3, 31)
    # End is the same as asof
    end = asof
    # Adjustments:
    # d1 = 30 (31 -> 30)
    # d2 = 30 (31 and d1 in {30,31} -> 30)
    # nod = (30-30) + 30*(3-1) + 360*0 = 60
    expected = Decimal(60) / Decimal(360)
    result = dcfc_30_360_us(start=start, asof=asof, end=end)
    assert result == expected
