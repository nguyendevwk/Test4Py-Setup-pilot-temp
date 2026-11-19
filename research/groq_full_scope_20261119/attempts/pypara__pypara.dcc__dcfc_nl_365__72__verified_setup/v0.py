import datetime
import decimal
import pytest

from pypara.dcc import dcfc_nl_365

# Helper to round Decimal to a given precision for comparison
def round_dec(value: decimal.Decimal, places: int) -> decimal.Decimal:
    return value.quantize(decimal.Decimal(f"1.{'0'*places}"))

def test_normal_examples():
    # Example 1 from docstring
    ex1_start = datetime.date(2007, 12, 28)
    ex1_asof = datetime.date(2008, 2, 28)
    result1 = dcfc_nl_365(start=ex1_start, asof=ex1_asof, end=ex1_asof)
    assert round_dec(result1, 14) == decimal.Decimal('0.16986301369863')

    # Example 2 from docstring (leap day)
    ex2_start = datetime.date(2007, 12, 28)
    ex2_asof = datetime.date(2008, 2, 29)
    result2 = dcfc_nl_365(start=ex2_start, asof=ex2_asof, end=ex2_asof)
    assert round_dec(result2, 14) == decimal.Decimal('0.16986301369863')

    # Example 3 from docstring
    ex3_start = datetime.date(2007, 10, 31)
    ex3_asof = datetime.date(2008, 11, 30)
    result3 = dcfc_nl_365(start=ex3_start, asof=ex3_asof, end=ex3_asof)
    assert round_dec(result3, 14) == decimal.Decimal('1.08219178082192')

def test_boundary_leap_year_transition():
    # Start on Feb 28 of a leap year, asof on Mar 1 of the same year
    start = datetime.date(2020, 2, 28)
    asof = datetime.date(2020, 3, 1)
    # Actual days: 2, but one leap day adjustment subtracts 1 => 1 day
    result = dcfc_nl_365(start=start, asof=asof, end=asof)
    assert round_dec(result, 14) == decimal.Decimal('0.00273972602740')  # 1/365

    # Start on Feb 28 of a non-leap year, asof on Mar 1
    start_nonleap = datetime.date(2019, 2, 28)
    asof_nonleap = datetime.date(2019, 3, 1)
    # No leap day adjustment
    result_nonleap = dcfc_nl_365(start=start_nonleap, asof=asof_nonleap, end=asof_nonleap)
    assert round_dec(result_nonleap, 14) == decimal.Decimal('0.00547945205479')  # 2/365

def test_zero_and_invalid_inputs():
    # asof equal to start should yield zero fraction
    start = datetime.date(2021, 5, 15)
    asof = start
    result_zero = dcfc_nl_365(start=start, asof=asof, end=asof)
    assert result_zero == decimal.Decimal('0')

    # asof before start should still compute negative fraction
    start_future = datetime.date(2022, 1, 1)
    asof_past = datetime.date(2021, 12, 31)
    result_negative = dcfc_nl_365(start=start_future, asof=asof_past, end=asof_past)
    # Actual days difference is -1, no leap day adjustment
    assert round_dec(result_negative, 14) == decimal.Decimal('-0.00273972602740')
