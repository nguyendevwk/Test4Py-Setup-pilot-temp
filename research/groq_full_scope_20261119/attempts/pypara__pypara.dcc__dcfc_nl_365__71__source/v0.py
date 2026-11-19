import datetime
import decimal
import pytest
from pypara.dcc import dcfc_nl_365
from pypara.commons.zeitgeist import Date

def test_normal_fraction_with_leap_day_adjustment():
    # Example from docstring: start 2007-12-28, asof 2008-02-29 (leap day)
    start = datetime.date(2007, 12, 28)
    asof = datetime.date(2008, 2, 29)
    end = asof
    result = dcfc_nl_365(start, asof, end)
    # Expected value from docstring rounded to 14 decimals
    expected = decimal.Decimal('0.16986301369863')
    assert result == expected

def test_fraction_over_multiple_years_without_leap_day():
    # Example from docstring: start 2008-02-01, asof 2009-05-31
    start = datetime.date(2008, 2, 1)
    asof = datetime.date(2009, 5, 31)
    end = asof
    result = dcfc_nl_365(start, asof, end)
    expected = decimal.Decimal('1.32602739726027')
    assert result == expected

def test_invalid_input_raises_type_error():
    # Passing a string instead of a Date should raise a TypeError when subtraction is attempted
    start = "2007-12-28"
    asof = datetime.date(2008, 2, 28)
    end = asof
    with pytest.raises(TypeError):
        dcfc_nl_365(start, asof, end)
