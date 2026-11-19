import datetime
from decimal import Decimal
import pytest

from pypara.dcc import dcfc_act_365_f


def test_normal_fraction_calculation():
    """
    Verify that the function returns the expected day count fraction for a
    typical period where the asof date is before the end date.
    """
    start = datetime.date(2020, 1, 1)
    asof = datetime.date(2020, 7, 1)   # 182 days from start
    end = datetime.date(2021, 1, 1)

    result = dcfc_act_365_f(start, asof, end)
    # 182 / 365 = 0.498630137
    assert isinstance(result, Decimal)
    assert round(result, 12) == Decimal('0.498630137')  # 182/365 rounded to 12 places


def test_boundary_case_asof_equals_end():
    """
    When the asof date equals the end date, the fraction should be the full
    period length divided by 365.
    """
    start = datetime.date(2019, 3, 15)
    asof = datetime.date(2020, 3, 15)
    end = datetime.date(2020, 3, 15)

    result = dcfc_act_365_f(start, asof, end)
    # 366 days in 2019-2020 leap year period
    assert round(result, 12) == Decimal('1.002739726')  # 366/365 rounded to 12 places


def test_invalid_input_raises_type_error():
    """
    Passing a non-date object should raise a TypeError because the function
    expects datetime.date instances.
    """
    start = datetime.date(2021, 1, 1)
    asof = "2021-06-01"  # invalid type
    end = datetime.date(2021, 12, 31)

    with pytest.raises(TypeError):
        dcfc_act_365_f(start, asof, end)
