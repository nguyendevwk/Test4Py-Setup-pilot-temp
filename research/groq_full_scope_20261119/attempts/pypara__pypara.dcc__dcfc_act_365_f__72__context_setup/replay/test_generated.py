import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_act_365_f, _get_actual_day_count


def test_dcfc_act_365_f_normal_case():
    """Test a typical calculation where the period spans a non‑leap year."""
    start = datetime.date(2023, 1, 1)
    asof = datetime.date(2023, 7, 1)
    end = datetime.date(2023, 7, 1)
    # 181 days from Jan 1 to Jul 1 (inclusive of start, exclusive of end)
    expected_fraction = Decimal(181) / Decimal(365)
    result = dcfc_act_365_f(start, asof, end)
    assert result == expected_fraction
    assert isinstance(result, Decimal)


def test_dcfc_act_365_f_boundary_leap_year():
    """Test a period that includes February 29 in a leap year."""
    start = datetime.date(2020, 2, 28)
    asof = datetime.date(2020, 3, 1)
    end = datetime.date(2020, 3, 1)
    # 2 days: Feb 28 -> Feb 29, Feb 29 -> Mar 1
    expected_fraction = Decimal(2) / Decimal(365)
    result = dcfc_act_365_f(start, asof, end)
    assert result == expected_fraction


def test_get_actual_day_count_error_and_zero():
    """Test that _get_actual_day_count returns 0 for same dates and raises for negative spans."""
    same = datetime.date(2021, 5, 15)
    assert _get_actual_day_count(same, same) == 0

    # Negative span should produce a negative number of days
    earlier = datetime.date(2021, 5, 14)
    later = datetime.date(2021, 5, 15)
    assert _get_actual_day_count(earlier, later) == 1
    assert _get_actual_day_count(later, earlier) == -1
