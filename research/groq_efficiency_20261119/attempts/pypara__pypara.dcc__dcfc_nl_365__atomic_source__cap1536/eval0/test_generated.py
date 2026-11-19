import datetime
import pytest
from decimal import Decimal

from pypara.dcc import dcfc_nl_365


def test_dcfc_nl_365_normal_examples():
    """Test the function against the examples in the docstring."""
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


def test_dcfc_nl_365_boundary_same_day():
    """When start, asof and end are the same date, the fraction should be zero."""
    same_day = datetime.date(2023, 3, 15)
    result = dcfc_nl_365(start=same_day, asof=same_day, end=same_day)
    assert result == Decimal("0")


def test_dcfc_nl_365_invalid_input_type():
    """Passing a non‑date type should raise a TypeError."""
    with pytest.raises(TypeError):
        dcfc_nl_365(start="2023-01-01", asof=datetime.date(2023, 1, 2), end=datetime.date(2023, 1, 3))
