import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_nl_365


def test_dcfc_nl_365_basic_examples():
    """Verify the function against the doctest examples."""
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


def test_dcfc_nl_365_zero_days():
    """When start and asof are the same date, the fraction should be zero."""
    d = datetime.date(2024, 1, 15)
    assert dcfc_nl_365(start=d, asof=d, end=d) == Decimal("0")


def test_dcfc_nl_365_negative_range():
    """If asof is before start, the function returns a negative fraction."""
    start = datetime.date(2024, 3, 1)
    asof = datetime.date(2024, 2, 28)  # one day before start
    end = datetime.date(2024, 3, 1)
    # The day count is -1, no leap day adjustment, so fraction is -1/365
    assert dcfc_nl_365(start=start, asof=asof, end=end) == Decimal("-1") / Decimal(365)
