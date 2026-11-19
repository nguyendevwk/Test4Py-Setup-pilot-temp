import datetime
from decimal import Decimal

import pytest

from pypara.dcc import dcfc_act_act


def test_normal_example_from_docstring():
    """Verify the function reproduces the example values from the docstring."""
    ex1_start, ex1_asof = datetime.date(2007, 12, 28), datetime.date(2008, 2, 28)
    ex2_start, ex2_asof = datetime.date(2007, 12, 28), datetime.date(2008, 2, 29)
    ex3_start, ex3_asof = datetime.date(2007, 10, 31), datetime.date(2008, 11, 30)
    ex4_start, ex4_asof = datetime.date(2008, 2, 1), datetime.date(2009, 5, 31)

    assert round(dcfc_act_act(start=ex1_start, asof=ex1_asof, end=ex1_asof), 14) == Decimal(
        "0.16942884946478"
    )
    assert round(dcfc_act_act(start=ex2_start, asof=ex2_asof, end=ex2_asof), 14) == Decimal(
        "0.17216108990194"
    )
    assert round(dcfc_act_act(start=ex3_start, asof=ex3_asof, end=ex3_asof), 14) == Decimal(
        "1.08243131970956"
    )
    assert round(dcfc_act_act(start=ex4_start, asof=ex4_asof, end=ex4_asof), 14) == Decimal(
        "1.32625945055768"
    )


def test_zero_length_period():
    """When start and asof are the same date, the fraction should be zero."""
    same_day = datetime.date(2024, 1, 15)
    result = dcfc_act_act(start=same_day, asof=same_day, end=same_day)
    assert result == Decimal("0")


def test_frequency_argument_is_ignored():
    """The optional freq argument should not influence the result."""
    start = datetime.date(2023, 1, 1)
    asof = datetime.date(2023, 7, 1)
    end = asof
    # Compute with freq=2 (semi‑annual) and freq=4 (quarterly)
    result_with_freq2 = dcfc_act_act(start=start, asof=asof, end=end, freq=Decimal("2"))
    result_with_freq4 = dcfc_act_act(start=start, asof=asof, end=end, freq=Decimal("4"))
    # The results must be identical
    assert result_with_freq2 == result_with_freq4
    # And they should match the expected fraction for a 181‑day period
    expected = Decimal("181") / Decimal("365")
    assert result_with_freq2 == expected
