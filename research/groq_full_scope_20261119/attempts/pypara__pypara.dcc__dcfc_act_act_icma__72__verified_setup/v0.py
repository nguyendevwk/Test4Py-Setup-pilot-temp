import datetime
import pytest
from decimal import Decimal

from pypara.dcc import dcfc_act_act_icma


def test_normal_case_example():
    """Test the example given in the docstring."""
    start = datetime.date(2019, 3, 2)
    asof = datetime.date(2019, 9, 10)
    end = datetime.date(2020, 3, 2)
    result = dcfc_act_act_icma(start=start, asof=asof, end=end)
    assert isinstance(result, Decimal)
    assert round(result, 10) == Decimal("0.5245901639")


def test_boundary_start_equals_end():
    """When start and end are the same, the fraction should be zero."""
    start = datetime.date(2021, 1, 1)
    asof = datetime.date(2021, 1, 1)
    end = datetime.date(2021, 1, 1)
    result = dcfc_act_act_icma(start=start, asof=asof, end=end)
    assert result == Decimal("0")


def test_error_asof_after_end():
    """The function should raise a ValueError if asof is after the end date."""
    start = datetime.date(2020, 1, 1)
    asof = datetime.date(2020, 12, 31)
    end = datetime.date(2020, 6, 30)
    with pytest.raises(ValueError):
        dcfc_act_act_icma(start=start, asof=asof, end=end)
