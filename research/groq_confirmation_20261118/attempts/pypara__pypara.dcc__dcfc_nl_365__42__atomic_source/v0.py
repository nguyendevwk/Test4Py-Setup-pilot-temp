import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_nl_365
from pypara.commons.zeitgeist import Date


def test_dcfc_nl_365_example_cases():
    """Verify the function against the examples in the docstring."""
    ex1_start, ex1_asof = datetime.date(2007, 12, 28), datetime.date(2008, 2, 28)
    ex2_start, ex2_asof = datetime.date(2007, 12, 28), datetime.date(2008, 2, 29)
    ex3_start, ex3_asof = datetime.date(2007, 10, 31), datetime.date(2008, 11, 30)
    ex4_start, ex4_asof = datetime.date(2008, 2, 1), datetime.date(2009, 5, 31)

    assert round(dcfc_nl_365(start=ex1_start, asof=ex1_asof, end=ex1_asof), 14) == Decimal(
        "0.16986301369863"
    )
    assert round(dcfc_nl_365(start=ex2_start, asof=ex2_asof, end=ex2_asof), 14) == Decimal(
        "0.16986301369863"
    )
    assert round(dcfc_nl_365(start=ex3_start, asof=ex3_asof, end=ex3_asof), 14) == Decimal(
        "1.08219178082192"
    )
    assert round(dcfc_nl_365(start=ex4_start, asof=ex4_asof, end=ex4_asof), 14) == Decimal(
        "1.32602739726027"
    )


def test_dcfc_nl_365_leap_day_adjustment():
    """The function should subtract one day when the period includes a leap day."""
    # Period that includes Feb 29, 2020
    start = datetime.date(2019, 12, 1)
    asof = datetime.date(2020, 3, 1)
    end = asof
    # Actual days between start and asof: 60 (Dec 1 to Mar 1)
    # Leap day adjustment: subtract 1 -> 59
    expected_fraction = Decimal(59) / Decimal(365)
    assert dcfc_nl_365(start=start, asof=asof, end=end) == expected_fraction

    # Period that does NOT include a leap day
    start_no_leap = datetime.date(2019, 12, 1)
    asof_no_leap = datetime.date(2020, 2, 1)
    end_no_leap = asof_no_leap
    # Actual days: 32 (Dec 1 to Feb 1)
    # No leap day adjustment
    expected_no_leap = Decimal(32) / Decimal(365)
    assert dcfc_nl_365(start=start_no_leap, asof=asof_no_leap, end=end_no_leap) == expected_no_leap


def test_dcfc_nl_365_zero_and_negative_periods():
    """When start equals asof the fraction should be zero; negative periods are allowed."""
    start = datetime.date(2021, 1, 1)
    asof = start
    end = asof
    assert dcfc_nl_365(start=start, asof=asof, end=end) == Decimal(0)

    # Negative period: asof before start
    start_neg = datetime.date(2021, 6, 1)
    asof_neg = datetime.date(2021, 5, 1)
    end_neg = asof_neg
    # Actual days: -31
    expected_neg = Decimal(-31) / Decimal(365)
    assert dcfc_nl_365(start=start_neg, asof=asof_neg, end=end_neg) == expected_neg
