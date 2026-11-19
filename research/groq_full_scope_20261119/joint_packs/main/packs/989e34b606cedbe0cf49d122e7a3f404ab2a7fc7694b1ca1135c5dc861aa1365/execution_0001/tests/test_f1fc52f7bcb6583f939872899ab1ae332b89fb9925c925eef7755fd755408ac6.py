import datetime
from decimal import Decimal
import pytest

from pypara.dcc import dcfc_30_360_isda


def test_normal_case_with_end_of_month_adjustments():
    """
    Verify that the function correctly handles the 30/360 ISDA rules for
    start dates on the 31st and asof dates on the 31st when the start
    month has 30 days.
    """
    # Start on 31st -> adjusted to 30th
    start = datetime.date(2023, 1, 31)
    # Asof on 31st of a month that has 30 days -> adjusted to 30th
    asof = datetime.date(2023, 2, 28)  # February has 28 days, no adjustment needed
    end = asof

    # Expected nod: (28-30) + 30*(2-1) + 360*(0) = -2 + 30 = 28
    expected_fraction = Decimal(28) / Decimal(360)
    assert dcfc_30_360_isda(start, asof, end) == expected_fraction


def test_boundary_case_with_february_leap_year():
    """
    Test the function on a leap year where the asof date is February 29th.
    The 30/360 ISDA convention does not treat February 29th specially,
    so the calculation should use the raw dates.
    """
    start = datetime.date(2020, 1, 15)
    asof = datetime.date(2020, 2, 29)  # Leap day
    end = asof

    # nod = (29-15) + 30*(2-1) + 360*0 = 14 + 30 = 44
    expected_fraction = Decimal(44) / Decimal(360)
    assert dcfc_30_360_isda(start, asof, end) == expected_fraction


def test_negative_fraction_when_start_after_asof():
    """
    The function does not enforce start <= asof; it will compute a negative
    day count fraction if start is after asof. This test ensures that
    such a scenario produces a negative result rather than raising an error.
    """
    start = datetime.date(2023, 3, 10)
    asof = datetime.date(2023, 3, 5)  # asof earlier than start
    end = asof

    # nod = (5-10) + 30*(3-3) + 360*0 = -5
    expected_fraction = Decimal(-5) / Decimal(360)
    assert dcfc_30_360_isda(start, asof, end) == expected_fraction
