import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_30_360_us


def test_normal_fraction_calculation():
    """Standard case where start and asof are not month ends."""
    start = datetime.date(2023, 1, 15)
    asof = datetime.date(2023, 4, 15)
    end = asof
    # Manual calculation: d1=15, d2=15, months=3, years=0
    nod = (15 - 15) + 30 * (4 - 1) + 360 * (2023 - 2023)  # 90
    expected = Decimal(nod) / Decimal(360)
    assert dcfc_30_360_us(start, asof, end) == expected
    assert expected == Decimal('0.25')


def test_last_day_of_month_adjustments():
    """Verify that last‑day‑of‑month dates are converted to 30 and 31→30 rules."""
    # start is last day of February (non‑leap year)
    start = datetime.date(2023, 2, 28)
    # asof is last day of March
    asof = datetime.date(2023, 3, 31)
    end = asof
    # d1 should become 30, d2 should become 30 (since asof is last day)
    nod = (30 - 30) + 30 * (3 - 2) + 360 * (2023 - 2023)  # 30
    expected = Decimal(nod) / Decimal(360)
    assert dcfc_30_360_us(start, asof, end) == expected
    assert expected == Decimal('0.0833333333333333')


def test_day_31_adjustment_and_boundary():
    """Check that a day 31 in the asof month is set to 30 when d1 is 30 or 31."""
    start = datetime.date(2023, 1, 31)
    asof = datetime.date(2023, 2, 28)  # d2=28, d1=31 → d1 becomes 30
    end = asof
    nod = (28 - 30) + 30 * (2 - 1) + 360 * (2023 - 2023)  # -2 + 30 = 28
    expected = Decimal(nod) / Decimal(360)
    assert dcfc_30_360_us(start, asof, end) == expected
    assert expected == Decimal('0.0777777777777778')
