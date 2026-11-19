import datetime
import pytest
from decimal import Decimal

# Import the target function from the package
from pypara.dcc import dcfc_30_360_german


def test_normal_case_example_1():
    """Test the example from the docstring (normal case)."""
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 28)
    end = asof
    result = dcfc_30_360_german(start=start, asof=asof, end=end)
    assert isinstance(result, Decimal)
    assert round(result, 14) == Decimal('0.16666666666667')


def test_boundary_case_february_end_of_month():
    """Test the special handling of February end‑of‑month dates."""
    # asof is Feb 28, end is Feb 28 -> d2 should stay 28
    start = datetime.date(2008, 1, 15)
    asof = datetime.date(2008, 2, 28)
    end_same = asof
    result_same = dcfc_30_360_german(start=start, asof=asof, end=end_same)
    # d2 = 28, d1 = 15 -> nod = (28-15)+30*(2-1)+360*(2008-2008)=13+30=43
    assert round(result_same, 14) == Decimal('0.11944444444444')

    # asof is Feb 28, end is Mar 1 -> d2 should be set to 30
    end_diff = datetime.date(2008, 3, 1)
    result_diff = dcfc_30_360_german(start=start, asof=asof, end=end_diff)
    # d2 = 30, d1 = 15 -> nod = (30-15)+30*(2-1)+360*(2008-2008)=15+30=45
    assert round(result_diff, 14) == Decimal('0.12500000000000')
    assert result_diff != result_same


def test_error_on_invalid_input_type():
    """Ensure that passing a non‑date type raises an AttributeError."""
    start = "2008-01-01"  # string, not a date
    asof = datetime.date(2008, 2, 1)
    end = datetime.date(2008, 3, 1)
    with pytest.raises(AttributeError):
        dcfc_30_360_german(start=start, asof=asof, end=end)
