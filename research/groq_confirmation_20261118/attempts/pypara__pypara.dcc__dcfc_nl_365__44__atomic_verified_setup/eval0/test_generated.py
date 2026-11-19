import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_nl_365


def test_normal_day_count_fraction():
    """Test a typical case where the period spans a non‑leap year."""
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 28)
    end = asof
    result = dcfc_nl_365(start=start, asof=asof, end=end)
    # Expected value from the docstring example
    expected = Decimal('0.16986301369863')
    assert result == expected, f"Expected {expected}, got {result}"


def test_boundary_same_start_and_asof():
    """Test the boundary case where start and asof are identical."""
    start = datetime.date(2024, 1, 1)
    asof = start
    end = asof
    result = dcfc_nl_365(start=start, asof=asof, end=end)
    # No days elapsed, so fraction should be zero
    assert result == Decimal('0'), f"Expected 0, got {result}"


def test_frequency_argument_is_ignored():
    """Test that the optional freq argument does not influence the result."""
    start = datetime.date(2023, 6, 15)
    asof = datetime.date(2023, 12, 15)
    end = asof
    # Compute with and without freq
    result_no_freq = dcfc_nl_365(start=start, asof=asof, end=end)
    result_with_freq = dcfc_nl_365(start=start, asof=asof, end=end, freq=Decimal('0.5'))
    assert result_no_freq == result_with_freq, (
        f"Result should be independent of freq: {result_no_freq} vs {result_with_freq}"
    )
