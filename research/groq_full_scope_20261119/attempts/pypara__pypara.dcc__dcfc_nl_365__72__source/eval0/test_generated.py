import datetime
from decimal import Decimal
import pytest

from pypara.dcc import dcfc_nl_365

# Helper to round Decimal to a fixed precision for comparison
def round_dec(value, places=14):
    return value.quantize(Decimal(f"1.{'0'*places}"))


def test_normal_day_count_fraction_examples():
    """Verify the function against the examples in the docstring."""
    ex1_start, ex1_asof = datetime.date(2007, 12, 28), datetime.date(2008, 2, 28)
    ex2_start, ex2_asof = datetime.date(2007, 12, 28), datetime.date(2008, 2, 29)
    ex3_start, ex3_asof = datetime.date(2007, 10, 31), datetime.date(2008, 11, 30)
    ex4_start, ex4_asof = datetime.date(2008, 2, 1), datetime.date(2009, 5, 31)

    assert round_dec(dcfc_nl_365(ex1_start, ex1_asof, ex1_asof)) == Decimal('0.16986301369863')
    assert round_dec(dcfc_nl_365(ex2_start, ex2_asof, ex2_asof)) == Decimal('0.16986301369863')
    assert round_dec(dcfc_nl_365(ex3_start, ex3_asof, ex3_asof)) == Decimal('1.08219178082192')
    assert round_dec(dcfc_nl_365(ex4_start, ex4_asof, ex4_asof)) == Decimal('1.32602739726027')


def test_leap_day_adjustment():
    """Check that a leap day between start and asof reduces the day count by one."""
    # Period that includes Feb 29, 2020
    start = datetime.date(2019, 12, 1)
    asof = datetime.date(2020, 3, 1)
    # Actual days between start and asof: 60 (Dec 1 to Mar 1)
    # Leap day adjustment: subtract 1 -> 59
    expected_fraction = Decimal(59) / Decimal(365)
    assert dcfc_nl_365(start, asof, asof) == expected_fraction


def test_negative_fraction_when_start_after_asof():
    """If start date is after asof, the function returns a negative fraction."""
    start = datetime.date(2021, 6, 1)
    asof = datetime.date(2021, 5, 1)
    # Actual days between start and asof: -31
    # No leap day adjustment because start > asof
    expected_fraction = Decimal(-31) / Decimal(365)
    assert dcfc_nl_365(start, asof, asof) == expected_fraction
