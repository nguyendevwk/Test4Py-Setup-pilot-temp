import datetime
import decimal
import pytest
from pypara.dcc import dcfc_act_365_f

def test_normal_fraction():
    # Standard case: 31 days between 2021-01-01 and 2021-02-01
    start = datetime.date(2021, 1, 1)
    asof = datetime.date(2021, 2, 1)
    end = asof
    result = dcfc_act_365_f(start, asof, end)
    expected = decimal.Decimal(31) / decimal.Decimal(365)
    assert result == expected
    assert isinstance(result, decimal.Decimal)

def test_leap_year_boundary():
    # Leap year: 29 days between 2020-02-01 and 2020-03-01
    start = datetime.date(2020, 2, 1)
    asof = datetime.date(2020, 3, 1)
    end = asof
    result = dcfc_act_365_f(start, asof, end)
    expected = decimal.Decimal(29) / decimal.Decimal(365)
    assert result == expected
    # Ensure fraction is greater than 0.079 (29/365)
    assert result > decimal.Decimal('0.079')

def test_negative_fraction_when_asof_before_start():
    # asof earlier than start yields negative fraction
    start = datetime.date(2021, 5, 1)
    asof = datetime.date(2021, 4, 1)
    end = asof
    result = dcfc_act_365_f(start, asof, end)
    expected = decimal.Decimal(-30) / decimal.Decimal(365)
    assert result == expected
    assert result < decimal.Decimal(0)
