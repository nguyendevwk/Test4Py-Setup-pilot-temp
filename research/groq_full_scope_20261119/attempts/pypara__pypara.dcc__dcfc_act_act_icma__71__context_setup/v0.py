import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_act_act_icma


def test_normal_fraction_calculation():
    """Verify that the function returns the expected fraction for a typical period."""
    start = datetime.date(2019, 3, 2)
    asof = datetime.date(2019, 9, 10)
    end = datetime.date(2020, 3, 2)
    # Expected value from the docstring example
    expected = Decimal("0.5245901639")
    result = dcfc_act_act_icma(start=start, asof=asof, end=end)
    assert result == expected, f"Expected {expected} but got {result}"


def test_fraction_with_custom_frequency():
    """Check that the optional frequency parameter correctly scales the result."""
    start = datetime.date(2021, 1, 1)
    asof = datetime.date(2021, 6, 30)
    end = datetime.date(2022, 1, 1)
    # Compute the fraction with the default frequency (1)
    default = dcfc_act_act_icma(start, asof, end)
    # Now use a frequency of 2 (e.g., semi‑annual)
    half = dcfc_act_act_icma(start, asof, end, freq=Decimal("2"))
    # The result with freq=2 should be exactly half of the default
    assert half == default / Decimal("2"), (
        f"With freq=2 the result should be half of the default: {half} vs {default / Decimal('2')}"
    )


def test_zero_denominator_raises():
    """When the period length is zero, the function should raise a ZeroDivisionError."""
    start = datetime.date(2023, 5, 15)
    asof = datetime.date(2023, 5, 15)
    end = datetime.date(2023, 5, 15)
    with pytest.raises(ZeroDivisionError):
        dcfc_act_act_icma(start, asof, end)
