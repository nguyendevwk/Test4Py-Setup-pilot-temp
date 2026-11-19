import datetime
import calendar
from decimal import Decimal
import pytest

from pypara.dcc import dcfc_nl_365, _has_leap_day, _get_actual_day_count


def test_dcfc_nl_365_normal_period():
    """
    Test a normal period that does not cross a leap day.
    The fraction should be the actual days divided by 365.
    """
    start = datetime.date(2023, 1, 1)
    asof = datetime.date(2023, 6, 30)
    end = asof
    # Actual days: 180 (Jan 1 to Jun 30 inclusive of start, exclusive of end)
    actual_days = _get_actual_day_count(start, asof)
    assert actual_days == 179  # 2023 is not a leap year
    # No leap day in range
    assert not _has_leap_day(start, asof)
    expected = Decimal(actual_days) / Decimal(365)
    result = dcfc_nl_365(start, asof, end)
    assert result == expected
    assert result == pytest.approx(Decimal('0.4904109589041095'))


def test_dcfc_nl_365_leap_day_inclusion():
    """
    Test a period that includes a leap day.
    The leap day should be subtracted from the day count.
    """
    start = datetime.date(2020, 1, 1)   # 2020 is a leap year
    asof = datetime.date(2020, 3, 1)
    end = asof
    # Actual days: 60 (Jan 1 to Mar 1 exclusive)
    actual_days = _get_actual_day_count(start, asof)
    assert actual_days == 59
    # Leap day 2020-02-29 is within the range
    assert _has_leap_day(start, asof)
    # The formula subtracts 1 for the leap day
    expected = (Decimal(actual_days) - Decimal(1)) / Decimal(365)
    result = dcfc_nl_365(start, asof, end)
    assert result == expected
    assert result == pytest.approx(Decimal('0.1589041095890411'))


def test_dcfc_nl_365_invalid_date_order():
    """
    Test that the function correctly handles an invalid date order
    where asof is before start. The convention should still return
    the fraction based on the actual days (negative days allowed).
    """
    start = datetime.date(2023, 6, 30)
    asof = datetime.date(2023, 1, 1)  # asof before start
    end = asof
    # Actual days: negative
    actual_days = _get_actual_day_count(start, asof)
    assert actual_days == -179
    # No leap day in this reversed range
    assert not _has_leap_day(start, asof)
    expected = Decimal(actual_days) / Decimal(365)
    result = dcfc_nl_365(start, asof, end)
    assert result == expected
    assert result == pytest.approx(Decimal('-0.4904109589041095'))
