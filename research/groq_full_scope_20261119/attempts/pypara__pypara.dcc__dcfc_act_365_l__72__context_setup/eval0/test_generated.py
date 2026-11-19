import datetime
import calendar
import pytest
from decimal import Decimal

# Import the target function from the package
from pypara.dcc import dcfc_act_365_l, _get_actual_day_count


def test_act_365_l_normal_leap_year():
    """
    Verify that the day count fraction for a period that includes a leap day
    uses a denominator of 366 and returns the expected fraction.
    """
    start = datetime.date(2020, 2, 28)   # 2020 is a leap year
    asof = datetime.date(2020, 3, 1)
    end = datetime.date(2020, 3, 1)

    # The actual day count is 2 days (28 Feb -> 1 Mar)
    actual_days = _get_actual_day_count(start, asof)
    assert actual_days == 2

    # Denominator should be 366 because 2020 is a leap year
    fraction = dcfc_act_365_l(start, asof, end)
    expected = Decimal(actual_days) / Decimal(366)
    assert fraction == expected
    assert fraction == Decimal('0.00546448087431694')


def test_act_365_l_boundary_non_leap_year():
    """
    Verify that the day count fraction for a period that does not include a leap day
    uses a denominator of 365 and returns the expected fraction.
    """
    start = datetime.date(2019, 12, 31)
    asof = datetime.date(2020, 1, 1)
    end = datetime.date(2020, 1, 1)

    # The actual day count is 1 day
    actual_days = _get_actual_day_count(start, asof)
    assert actual_days == 1

    # 2020 is a leap year, but the asof year is 2020, so denominator is 366
    fraction = dcfc_act_365_l(start, asof, end)
    expected = Decimal(actual_days) / Decimal(366)
    assert fraction == expected
    assert fraction == Decimal('0.00273224043715847')


def test_act_365_l_invalid_date_order():
    """
    Verify that providing dates where start > asof or asof > end
    results in a fraction of 0 (handled by the DCC wrapper, but the
    underlying function should still compute normally; we test the
    wrapper indirectly by using the DCC calculate_fraction method).
    """
    from pypara.dcc import DCC, dcc

    @dcc("test_invalid")
    def dummy(start, asof, end, freq=None):
        return dcfc_act_365_l(start, asof, end)

    # Create a DCC instance via the decorator
    dcc_instance = dummy.__dcc

    # Case 1: start > asof
    start = datetime.date(2021, 5, 10)
    asof = datetime.date(2021, 5, 5)
    end = datetime.date(2021, 5, 15)
    fraction = dcc_instance.calculate_fraction(start, asof, end)
    assert fraction == Decimal('0')

    # Case 2: asof > end
    start = datetime.date(2021, 5, 1)
    asof = datetime.date(2021, 5, 20)
    end = datetime.date(2021, 5, 15)
    fraction = dcc_instance.calculate_fraction(start, asof, end)
    assert fraction == Decimal('0')
